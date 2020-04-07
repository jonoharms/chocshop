from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Role, User, Product, Purchase

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')])
    building = StringField('Building', validators=[Length(0, 64)])
    room = StringField('Room', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')])
    building = StringField('Building', validators=[Length(0, 64)])
    room = StringField('Room', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class AddNewProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(0,64)])
    barcode = StringField('Barcode', validators=[DataRequired(), Length(0,64)])
    current_price = DecimalField('Current Price', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Product.query.filter_by(name=field.data).first():
            raise ValidationError('Product name already registered.')

    def validate_barcode(self, field):
        if Product.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')