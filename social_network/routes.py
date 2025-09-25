# from app import app, db, login_manager
# from flask import render_template, redirect, url_for, flash, request
# from flask_login import login_user, logout_user, login_required, current_user
# from forms import RegistrationForm, LoginForm, EditProfileForm, PostForm, CommentForm, MessageForm, SearchForm
# from models import User, Post, Like, Comment, Message
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         posts = current_user.followed_posts().all()
#     else:
#         posts = Post.query.order_by(Post.timestamp.desc()).all()
#     return render_template('index.html', posts=posts)
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('ثبت‌نام با موفقیت انجام شد! اکنون وارد شوید.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             flash('خوش آمدید!', 'success')
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('index'))
#         else:
#             flash('ایمیل یا رمز عبور اشتباه است.', 'danger')
#     return render_template('login.html', form=form)
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('شما از حساب خود خارج شدید.', 'info')
#     return redirect(url_for('index'))
#
# @app.route('/profile/<username>')
# @login_required
# def profile(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = user.posts.order_by(Post.timestamp.desc()).all()
#     return render_template('profile.html', user=user, posts=posts)
#
# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(obj=current_user)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.bio = form.bio.data
#         db.session.commit()
#         flash('اطلاعات پروفایل با موفقیت بروزرسانی شد.', 'success')
#         return redirect(url_for('profile', username=current_user.username))
#     return render_template('edit_profile.html', form=form)
#
# @app.route('/create_post', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(body=form.body.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('پست شما منتشر شد!', 'success')
#         return redirect(url_for('index'))
#     return render_template('create_post.html', form=form)
#
# @app.route('/like/<int:post_id>')
# @login_required
# def like_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
#     if like:
#         # اگر قبلا لایک کرده بود، حذفش کن (آن‌لایک)
#         db.session.delete(like)
#         db.session.commit()
#         flash('لایک حذف شد.', 'info')
#     else:
#         new_like = Like(user_id=current_user.id, post_id=post.id)
#         db.session.add(new_like)
#         db.session.commit()
#         flash('پست را لایک کردی!', 'success')
#     return redirect(request.referrer or url_for('index'))
#
# @app.route('/post/<int:post_id>', methods=['GET', 'POST'])
# @login_required
# def post_detail(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post.id)
#         db.session.add(comment)
#         db.session.commit()
#         flash('نظر شما ثبت شد.', 'success')
#         return redirect(url_for('post_detail', post_id=post.id))
#     comments = post.comments.order_by(Comment.timestamp.asc()).all()
#     return render_template('post_detail.html', post=post, comments=comments, form=form)
#
# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     if user == current_user:
#         flash('نمی‌توانید خودتان را دنبال کنید!', 'warning')
#         return redirect(url_for('profile', username=username))
#     current_user.follow(user)
#     db.session.commit()
#     flash(f'شما {username} را دنبال کردید.', 'success')
#     return redirect(url_for('profile', username=username))
#
# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     if user == current_user:
#         flash('نمی‌توانید خودتان را از دنبال کردن خارج کنید!', 'warning')
#         return redirect(url_for('profile', username=username))
#     current_user.unfollow(user)
#     db.session.commit()
#     flash(f'شما {username} را از دنبال شده‌ها حذف کردید.', 'info')
#     return redirect(url_for('profile', username=username))
#
# @app.route('/send_message/<username>', methods=['GET', 'POST'])
# @login_required
# def send_message(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     form = MessageForm()
#     if form.validate_on_submit():
#         msg = Message(sender=current_user, recipient=user, body=form.body.data)
#         db.session.add(msg)
#         db.session.commit()
#         flash('پیام شما ارسال شد.', 'success')
#         return redirect(url_for('profile', username=username))
#     return render_template('send_message.html', form=form, recipient=user)
#
# @app.route('/messages')
# @login_required
# def messages():
#     received_msgs = current_user.received_messages.order_by(Message.timestamp.desc()).all()
#     return render_template('messages.html', messages=received_msgs)
#
# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# def search():
#     form = SearchForm()
#     users = []
#     if form.validate_on_submit():
#         query = form.username.data
#         users = User.query.filter(User.username.ilike(f'%{query}%')).all()
#     return render_template('search.html', form=form, users=users)
