from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
import pymongo

c = pymongo.Connection()
db = c['users']

class ContactForm(Form):
    name = TextField("Name",
                     [validators.Required("Please enter your name.")])
    email = TextField("Email",
                      [validators.Required("Please enter your email address."),
                       validators.Email("Please enter your email address.")])
    subject = TextField("Subject",
                        [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message",
                            [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")

class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email.")])
    password = PasswordField("Password", [validators.Required("Please enter your password.")])
    submit = SubmitField("Create Account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = db.user.find_one({"email": self.email.data.lower()})
        if user:
            self.email.errors.append("That email is already taken.")
            return False
        else:
            return True

class SigninForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email.")])
    password = PasswordField("Password", [validators.Required("Please enter your password.")])
    submit = SubmitField("Sign in")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = db.user.find_one({"email": self.email.data.lower()})
        if user and user['password'] == self.password.data:
            return True
        else:
            self.email.errors.append("Invalid email or password")
            return False
