from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class SimpleLoginForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z0-9_.]*$', 0,
               'Barcodes must have only letters, numbers, dots or '
               'underscores')],render_kw={'autofocus': True})
    submit = SubmitField('Log In')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    barcode = StringField('Barcode', validators=[
        DataRequired(), Length(1, 64),
        Regexp('[A-Za-z0-9_.]*$', 0,
               'Barcodes must have only letters, numbers, dots or '
               'underscores')])
    name = StringField('Real name', validators=[Length(0, 64),DataRequired()])
    balance = DecimalField('Initial Balance', default=0.00, places=2)
  #  site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')],validators=[DataRequired()])
  #  building = StringField('Building', validators=[Length(0, 64),DataRequired()])
  #  room = StringField('Room', validators=[Length(0, 64),DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    
    def validate_barcode(self, field):
        if User.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')