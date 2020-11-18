from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from models import User, Question, Category
from exceptions import ValidationError

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from functools import partial
from sqlalchemy import orm


def get_category(columns=None):
    category = Category.query
    if columns:
        category = category.options(orm.load_only(*columns))
    return category


def get_category_factory(columns=None):
    return partial(get_category, columns=columns)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,64), Regexp('^[a-zA-Z0-9_.-]*$',0,'Usernames must only have letters, numbers, dots or underscores')], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Confirm password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('An account with this email already exists.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username already exists. Please use a different username.')


class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators=[DataRequired()])
    #body = PageDownField('Add a new Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('1', 'Easy'), ('2', 'Medium'), ('3', 'Difficult')])
    category = QuerySelectField(query_factory=get_category_factory(['id', 'type']), get_label='type')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_category(self, field):
        if Category.query.filter_by(type=field.data).first():
            raise ValidationError('This category already exists. Please use a different category.')