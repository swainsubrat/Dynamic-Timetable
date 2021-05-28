from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from flaskblog.models import User


highest_qualification = [
    ("matriculation", "10th"),
    ("twelveth", "+2"),
    ("graduation", "Graduation"),
    ("masters", "Post-graduation")
]


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    subject = StringField('Subject',
                           validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.'
            )


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResumeForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=40)]
    )
    number = StringField(
        'Number',
        validators=[DataRequired(), Length(min=10, max=10)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    qualification = SelectField(
        'Qualification',
        choices=highest_qualification
    )
    resume = FileField(validators=[
        FileRequired(),
        FileAllowed(["pdf"], "Pdfs only!")
    ])
    submit = SubmitField('Apply')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.'
            )
