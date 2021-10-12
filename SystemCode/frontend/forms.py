from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectMultipleField, FieldList, \
    validators, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


class SignupForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=1, max=200)])
    username = StringField('Username',validators=[DataRequired(),Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class SurveyForm(FlaskForm):
    topic = StringField('What would you like to learn?',validators=[DataRequired(), Length(min=0, max=200)])
    duration = RadioField('Duration*', choices=[(1,'Short (1 - 10 hours)'),(2,'Medium (10 - 50 hours)'),(3,'Long (>50 hours)'),(0,'No preference')])
    difficulty = RadioField('Difficulty level*', choices=[(0, 'Any'),(1, 'Beginner'),(2, 'Intermediate'), (3, 'Advanced')])
    freePaid = RadioField('Would you be open to paid courses?*',
                          choices=[(0, 'Yes. Show me both paid and free courses'),
                                   (1, 'No. Show me free courses only')], coerce=str)
    recommend = SubmitField('Get courses')