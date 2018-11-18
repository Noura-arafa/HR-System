from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LogInForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateForm (FlaskForm):
    employeeID = IntegerField('Employee ID', validators=[DataRequired()])
    present = BooleanField('Present')
    absent = BooleanField('absent')
    dayOFF = BooleanField('Day OFF')
    sickLeave = BooleanField('Sick Leave')
    workingHours = IntegerField('Working hours')
    submit = SubmitField('Update')


class DeleteForm (FlaskForm):
    employeeID = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Delete')