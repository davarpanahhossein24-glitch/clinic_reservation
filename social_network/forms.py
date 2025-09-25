# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
# try:
#     from models import User
# except ImportError:
#     User = None
#
# from flask_wtf import FlaskForm
# from wtforms import TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Length
# from wtforms import StringField
#
# class RegistrationForm(FlaskForm):
#     username = StringField('نام کاربری', validators=[DataRequired()])
#     email = StringField('ایمیل', validators=[DataRequired(), Email()])
#     password = PasswordField('رمز عبور', validators=[DataRequired()])
#     confirm_password = PasswordField('تایید رمز عبور', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('ثبت نام')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('این نام کاربری قبلا ثبت شده است.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('این ایمیل قبلا ثبت شده است.')
#
# class LoginForm(FlaskForm):
#     email = StringField('ایمیل', validators=[DataRequired(), Email()])
#     password = PasswordField('رمز عبور', validators=[DataRequired()])
#     submit = SubmitField('ورود')
#
# class EditProfileForm(FlaskForm):
#     username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=25)])
#     bio = TextAreaField('درباره من', validators=[Length(max=255)])
#     submit = SubmitField('ذخیره تغییرات')
#
#
# class PostForm(FlaskForm):
#     body = TextAreaField('متن پست', validators=[DataRequired(), Length(min=1, max=500)])
#     submit = SubmitField('ارسال')
#
# class CommentForm(FlaskForm):
#     body = TextAreaField('نظر شما', validators=[DataRequired(), Length(min=1, max=300)])
#     submit = SubmitField('ارسال نظر')
#
# class MessageForm(FlaskForm):
#     body = TextAreaField('پیام', validators=[DataRequired(), Length(min=1, max=1000)])
#     submit = SubmitField('ارسال پیام')
#
# class SearchForm(FlaskForm):
#     username = StringField('نام کاربری', validators=[DataRequired()])
#     submit = SubmitField('جستجو')