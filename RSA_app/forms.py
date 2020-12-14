from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from RSA_app.database import Restaurant
from wtforms_components import TimeField


class RegistrationForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[
                        DataRequired(), Length(min=2, max=100)])
    restaurant_email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_signup = SubmitField('Sign Up')

    # Unique Account Per Restaurant Only:
    def validate_account(self, restaurant_email, restaurant_name):
        email = Restaurant.query.filter_by(email=restaurant_email.data).all()
        name = Restaurant.query.filter_by(name=restaurant_name.data).all()
        if email or name:
            raise ValidationError('This restaurant already has an account!')


def validate_account(restaurant_email, restaurant_name):
    email = Restaurant.query.filter_by(email=restaurant_email.data).all()
    name = Restaurant.query.filter_by(name=restaurant_name.data).all()
    if email or name:
        raise ValidationError('This restaurant already has an account!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_login = SubmitField('Login')


class UpdateContactInfo(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email()])
    name = StringField('Restaurant Name', validators=[Optional(), Length(min=2, max=100)])
    address = StringField('Restaurant Address')
    phone = IntegerField('Phone Number', [Optional()])
    type = StringField('Food Type')
    cost = StringField('Cost Level')
    capacity = IntegerField('Set New Capacity', [Optional()])
    update_profile = SubmitField('Update')

    # Unique Account Per Restaurant Only:
    def validate_account(self, restaurant_email, restaurant_name):
        email = Restaurant.query.filter_by(email=restaurant_email.data).all()
        name = Restaurant.query.filter_by(name=restaurant_name.data).all()
        if email or name:
            raise ValidationError('This restaurant already has an account!')


class UpdateAvailability(FlaskForm):
    capacity = IntegerField('Update Total Capacity', [Optional()])

    # Monday
    mon_start = TimeField('Monday', [Optional()], format='%H:%M')
    mon_end = TimeField('', [Optional()], format='%H:%M')

    # Tuesday
    tues_start = TimeField('Tuesday', [Optional()], format='%H:%M')
    tues_end = TimeField('', [Optional()], format='%H:%M')

    # Wednesday
    wed_start = TimeField('Wednesday', [Optional()], format='%H:%M')
    wed_end = TimeField('', [Optional()], format='%H:%M')

    # Thursday
    th_start = TimeField('Thursday', [Optional()], format='%H:%M')
    th_end = TimeField('', [Optional()], format='%H:%M')

    # Friday
    fri_start = TimeField('Friday', [Optional()], format='%H:%M')
    fri_end = TimeField('', [Optional()], format='%H:%M')

    # Saturday
    sat_start = TimeField('Saturday', [Optional()], format='%H:%M')
    sat_end = TimeField('', [Optional()], format='%H:%M')

    # Sunday
    sun_start = TimeField('Sunday', [Optional()], format='%H:%M')
    sun_end = TimeField('', [Optional()], format='%H:%M')

    submit_schedule = SubmitField('Submit')


class AddMenuItem(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    ing = TextAreaField('Ingredients', [Optional()])
    allergens = TextAreaField('Allergens', [Optional()])
    price = DecimalField('Price: $', [Optional()])
    avl = BooleanField('Currently Available?', [Optional()])
    add_menu_item = SubmitField('Add New Item')
