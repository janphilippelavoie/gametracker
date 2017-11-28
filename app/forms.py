from wtforms import Form, StringField, PasswordField
from wtforms import validators


class SignupForm(Form):
    username = StringField('Username', [validators.Length(4)])
    email = StringField('Email Address', [validators.Email()])
    password = PasswordField('Password', [
        validators.Length(4),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    email = StringField('Email')
    password = StringField('Password')
