from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from flask_login import current_user
from work_hours_app.models import User
    

class LoginForm(FlaskForm):
    username_or_email = StringField("Username_email", validators=[DataRequired()])
    # username = StringField("Username")
    # email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    username = StringField("Username")
    firstname = StringField("First Name")
    lastname = StringField("Last Name")
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("pass_confirm", message = "Passwords must match")])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Your email has been registered already!")
        
    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Your username has been registered already!")

class AddUserForm(RegisterForm):
    is_admin = BooleanField("Admin")


class UpdateUserForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    username = StringField("Username")
    submit = SubmitField("Update")

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Your email has been registered already!")
        

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Your username has been registered already!")
          