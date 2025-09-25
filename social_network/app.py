from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf.file import FileField, FileAllowed
import secrets
from PIL import Image
from sqlalchemy import func
from werkzeug.utils import secure_filename

# =======================
# تنظیمات و ساخت اپلیکیشن
# =======================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-very-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# =======================
# مدل‌ها
# =======================

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.String(255))
    profile_image = db.Column(db.String(255), default='default.jpg')

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

def create_notification(user, message):
    notif = Notification(user=user, message=message)
    db.session.add(notif)
    db.session.commit()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hashtags = db.Column(db.String(255))

    likes = db.relationship('Like', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class EditProfileForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=25)])
    bio = TextAreaField('درباره من', validators=[Length(max=255)])
    profile_image = FileField('آپلود عکس پروفایل', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'فقط فایل‌های تصویری مجاز هستند!')])
    submit = SubmitField('ذخیره تغییرات')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # گیرنده نوتیفیکیشن
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='notifications')

# =======================
# فرم‌ها
# =======================

class RegistrationForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    password2 = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password', message='رمز عبور باید یکی باشد')])
    submit = SubmitField('ثبت نام')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلا ثبت شده است.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('این ایمیل قبلا ثبت شده است.')

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

class EditProfileForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=25)])
    bio = TextAreaField('درباره من', validators=[Length(max=255)])
    submit = SubmitField('ذخیره تغییرات')

class PostForm(FlaskForm):
    body = TextAreaField('متن پست', validators=[DataRequired(), Length(min=1, max=500)])
    hashtags = StringField('هشتگ‌ها (با کاما جدا کنید)')
    submit = SubmitField('ارسال')


class CommentForm(FlaskForm):
    body = TextAreaField('نظر شما', validators=[DataRequired(), Length(min=1, max=300)])
    submit = SubmitField('ارسال نظر')

class MessageForm(FlaskForm):
    body = TextAreaField('پیام', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('ارسال پیام')

class SearchForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    submit = SubmitField('جستجو')

# =======================
# بارگذاری یوزر برای Flask-Login
# =======================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =======================
# روت‌ها
# =======================

@app.route('/')
def index():
    if current_user.is_authenticated:
        # مرتب کردن پست‌ها براساس تعداد لایک (نزولی)
        posts = Post.query.outerjoin(Like).group_by(Post.id).order_by(func.count(Like.id).desc()).all()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ثبت‌نام با موفقیت انجام شد! اکنون وارد شوید.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('خوش آمدید!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('ایمیل یا رمز عبور اشتباه است.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('شما از حساب خود خارج شدید.', 'info')
    return redirect(url_for('index'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data

        if form.profile_image.data:
            # تولید اسم تصادفی برای جلوگیری از تکراری بودن اسم فایل
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.profile_image.data.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)

            # ذخیره فایل
            form.profile_image.data.save(picture_path)

            # ذخیره اسم عکس در دیتابیس
            current_user.profile_image = picture_fn

        db.session.commit()
        flash('اطلاعات پروفایل با موفقیت بروزرسانی شد.', 'success')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('edit_profile.html', form=form)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, hashtags=form.hashtags.data)
        db.session.add(post)
        db.session.commit()
        flash('پست شما منتشر شد!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/like/<int:post_id>')
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('لایک حذف شد.', 'info')
    else:
        new_like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        db.session.commit()
        flash('پست را لایک کردی!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('نظر شما ثبت شد.', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    if post.author != current_user:
        create_notification(post.author, f'{current_user.username} برای پست شما نظر گذاشت.')

    comments = post.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('post_detail.html', post=post, comments=comments, form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash('نمی‌توانید خودتان را دنبال کنید!', 'warning')
        return redirect(url_for('profile', username=username))
    current_user.follow(user)
    create_notification(user, f'{current_user.username} شما را دنبال کرد.')
    db.session.commit()
    flash(f'شما {username} را دنبال کردید.', 'success')
    return redirect(url_for('profile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash('نمی‌توانید خودتان را از دنبال کردن خارج کنید!', 'warning')
        return redirect(url_for('profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'شما {username} را از دنبال شده‌ها حذف کردید.', 'info')
    return redirect(url_for('profile', username=username))

@app.route('/send_message/<username>', methods=['GET', 'POST'])
@login_required
def send_message(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user, body=form.body.data)
        db.session.add(msg)
        db.session.commit()
        flash('پیام شما ارسال شد.', 'success')
        return redirect(url_for('profile', username=username))
    create_notification(user, f'{current_user.username} برای شما پیام فرستاد.')
    return render_template('send_message.html', form=form, recipient=user)

@app.route('/messages')
@login_required
def messages():
    received_msgs = current_user.received_messages.order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', messages=received_msgs)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    users = []
    if form.validate_on_submit():
        query = form.username.data
        users = User.query.filter(User.username.ilike(f'%{query}%')).all()
    return render_template('search.html', form=form, users=users)

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # تغییر اندازه عکس به 125x125 برای بهینه بودن
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

@app.route('/notifications')
@login_required
def notifications():
    notifs = current_user.notifications.order_by(Notification.timestamp.desc()).all()

    # همه رو خونده کنیم
    for notif in notifs:
        notif.is_read = True
    db.session.commit()

    return render_template('notifications.html', notifications=notifs)

@app.route('/inbox')
@login_required
def inbox():
    # لیست کاربران که با آنها پیام رد و بدل شده
    # پیام‌های فرستاده شده یا دریافتی current_user
    user_ids = set()
    sent = Message.query.filter_by(sender_id=current_user.id).all()
    received = Message.query.filter_by(recipient_id=current_user.id).all()

    for msg in sent:
        user_ids.add(msg.recipient_id)
    for msg in received:
        user_ids.add(msg.sender_id)

    users = User.query.filter(User.id.in_(list(user_ids))).all()
    return render_template('inbox.html', users=users)

@app.route('/chat/<username>', methods=['GET', 'POST'])
@login_required
def chat(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user, body=form.body.data)
        db.session.add(msg)
        db.session.commit()
        flash('پیام ارسال شد.', 'success')
        return redirect(url_for('chat', username=username))

    # گرفتن پیام‌های دوطرفه (current_user و user)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == user.id)) |
        ((Message.sender_id == user.id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('chat.html', form=form, messages=messages, user=user)

# =======================
# اجرای اپلیکیشن
# =======================

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
