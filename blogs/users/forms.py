from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from blogs.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'pass_confirm', message='Passwords must match'), Length(min=8, max=16)])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'The email you chose has already been registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'The username yuo chose has already been registered')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError(
                    'The email you chose has already been registered')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError(
                    'The username you chose has already been registered')


class PredictionForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[
                        ('0', 'Male'), ('1', 'Female'), ('2', 'Trans')])
    family_history = RadioField('Family History of Mental Illness', choices=[
                                ('1', 'Yes'), ('0', 'No')])
    self_employed = RadioField('Are you Self Employed?', choices=[
                               ('1', 'Yes'), ('0', 'No')])
    remote_work = RadioField('Do you work remotely?',
                             choices=[('1', 'Yes'), ('0', 'No')])
    tech_company = RadioField('Do you work in a tech company?', choices=[
                              ('1', 'Yes'), ('0', 'No')])
    coworkers = RadioField('Has any of your coworkers suffered from any mental illness?',
                           choices=[('1', 'Yes'), ('0', 'No'), ('2', "Don't Know")])
    wellness_program = RadioField('Have you been a part of any wellness program?', choices=[
                                  ('1', 'Yes'), ('0', 'No'), ('2', "Don't Know")])

    submit = SubmitField('Submit')
