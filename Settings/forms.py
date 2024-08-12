from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length

class CompanySettingsForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=255)])
    short_name = StringField('Short Name', validators=[DataRequired(), Length(max=50)])
    logo = FileField('Logo')
    address = TextAreaField('Address')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    tel = StringField('Telephone', validators=[Length(max=20)])
    website = StringField('Website', validators=[Length(max=100)])
