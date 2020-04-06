from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    site = SelectField('Site', choices=[('FMB','Fishermand Bend'), ('EDN', 'Edinburgh'),('OTH', 'Other')])
    building = StringField('Building', validators=[Length(0, 64)])
    room = StringField('Room', validators=[Length(0, 64)])
    submit = SubmitField('Submit')