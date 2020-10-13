from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from wtforms import ValidationError
from ..models import Role, User, Product, Purchase

class BuyForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired(), Length(0, 64)],render_kw={'autofocus': True})
    buy = SubmitField('Buy')

    def validate_barcode(self, field):
        if not Product.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode Not Valid')

class TopUpForm(FlaskForm):
    amount = DecimalField('Amount', default=0.00,places=2, validators=[DataRequired()])
    topup = SubmitField('Top Up')
    

class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators=[Length(0, 64)])
    barcode = StringField('Barcode', validators=[
        DataRequired(), Length(1, 64),
        Regexp('[A-Za-z0-9_.]*$', 0,
               'Barcodes must have only letters, numbers, dots or '
               'underscores')])
  #  site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')])
  #  building = StringField('Building', validators=[Length(0, 64)])
  #  room = StringField('Room', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_barcode(self, field):
        if field.data != self.user.barcode and \
                User.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')


class EditProfileAdminForm(FlaskForm):
   # email = StringField('Email')
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
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
 #   site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')])
 #   building = StringField('Building', validators=[Length(0, 64)])
 #   room = StringField('Room', validators=[Length(0, 64)])
    balance = DecimalField('Balance', default=0.00, places=2)
    submit = SubmitField('Submit')
    

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    # def validate_email(self, field):
    #     if field.data != self.user.email and \
    #             User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    
    def validate_barcode(self, field):
        if field.data != self.user.barcode and \
                User.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')


class AddNewProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(0,64)])
    description = StringField('Description', validators=[Length(0,128)], default=None)
    barcode = StringField('Barcode', validators=[DataRequired(), Length(0,64)])
    current_price = DecimalField('Current Price', places=2, validators=[DataRequired()])
    url = StringField('Icon URL', validators=[Length(0,128)])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Product.query.filter_by(name=field.data).first():
            raise ValidationError('Product name already registered.')

    def validate_barcode(self, field):
        if Product.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')


class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(0,64)])
    description = StringField('Description', validators=[Length(0,128)], default=None)
    barcode = StringField('Barcode', validators=[DataRequired(), Length(0,64)])
    current_price = DecimalField('Current Price', places=2, validators=[DataRequired()])
    url = StringField('Icon URL', validators=[Length(0,128)])
    submit = SubmitField('Submit')

    def __init__(self, product, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.product = product

    def validate_name(self, field):
        if field.data != self.product.name and \
                Product.query.filter_by(name=field.data).first():
            raise ValidationError('Product name already registered.')

    def validate_barcode(self, field):
        if field.data != self.product.barcode and \
                Product.query.filter_by(barcode=field.data).first():
            raise ValidationError('Barcode already in use.')


