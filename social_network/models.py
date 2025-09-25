# from extensions import db
# # بقیه کد مدل‌ها ...
# from flask_login import UserMixin
# from datetime import datetime
#
# followers = db.Table('followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )
#
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     bio = db.Column(db.String(255))
#     profile_image = db.Column(db.String(255), default='default.jpg')
#
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#     likes = db.relationship('Like', backref='user', lazy='dynamic')
#     comments = db.relationship('Comment', backref='user', lazy='dynamic')
#
#     followed = db.relationship(
#         'User', secondary=followers,
#         primaryjoin=(followers.c.follower_id == id),
#         secondaryjoin=(followers.c.followed_id == id),
#         backref=db.backref('followers', lazy='dynamic'),
#         lazy='dynamic'
#     )
#
#     def set_password(self, password):
#         from werkzeug.security import generate_password_hash
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         from werkzeug.security import check_password_hash
#         return check_password_hash(self.password_hash, password)
#
#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)
#
#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)
#
#     def is_following(self, user):
#         return self.followed.filter(
#             followers.c.followed_id == user.id
#         ).count() > 0
#
#     def followed_posts(self):
#         followed = Post.query.join(
#             followers, (followers.c.followed_id == Post.user_id)
#         ).filter(followers.c.follower_id == self.id)
#         own = Post.query.filter_by(user_id=self.id)
#         return followed.union(own).order_by(Post.timestamp.desc())
#
#
#
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     body = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
#     recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     likes = db.relationship('Like', backref='post', lazy='dynamic')
#     comments = db.relationship('Comment', backref='post', lazy='dynamic')
#
#
#
# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#
#
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
