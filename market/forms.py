from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError("Username has already exist, Please try to another username!!!")

    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_address = email_address_to_check.data).first()

        if email_address:
            raise ValidationError("Email Address has already exist, Please try to another email address!!!")


    username = StringField(label = 'Username :', validators=[Length(min=6,max=30),DataRequired()])
    email_address = EmailField(label='Email Address :', validators=[Email(),DataRequired()])
    password1 = PasswordField(label = 'Password :', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password :', validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label = 'Register')



class LoginForm(FlaskForm):
    username = StringField(label = "Username :", validators=[DataRequired()])
    password = PasswordField(label = "Password :", validators=[DataRequired()])
    submit = SubmitField(label = 'Login')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label = 'Purchase')


class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')



