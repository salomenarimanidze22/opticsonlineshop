from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, DataRequired, Length, Email, EqualTo

from models import User


class AddProduct(FlaskForm):
    name = StringField(label="Name", validators=[Length(min=2), DataRequired()])
    file = StringField(label="File")
    price = IntegerField(label="Price")
    submit = SubmitField(label="Submit")

    def __str__(self):
        return f"{self.name}"
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ეს სახელი დაკავებულია, შეიყვანეთ სხვა')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



    