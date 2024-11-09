from wtforms import Form, BooleanField, StringField, validators, PasswordField

class RegistrationForm(Form):
    email = StringField('Email Address')
    password = PasswordField('Password')
    accept_rules = BooleanField('I accept the site rules')