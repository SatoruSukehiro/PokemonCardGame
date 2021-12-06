from flask_wtf import FlaskForm
from wtforms import Form,StringField,FloatField,SubmitField,DateField, SelectField,IntegerField





class Register(FlaskForm):
    ''' Register User Form'''

    username = StringField('Username')
    password = StringField('Password')
    luckynum = IntegerField('Whats Your Lucky Number?')
    email = StringField('Email')
    starter = SelectField('Choose Your Starter')
    submit = SubmitField('Complete Registration')


