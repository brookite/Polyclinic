from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo
from app.db.authorization import get_user
import phonenumbers


class LoginForm(FlaskForm):
    login = StringField("Имя пользователя: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    submit = SubmitField("Войти")


class PatientRegisterForm(FlaskForm):
    login = StringField("Имя пользователя: ", validators=[DataRequired(), Length(5, 16)])
    first_name = StringField("Имя: ", validators=[DataRequired(), Length(2, 24)])
    middle_name = StringField("Отчество: ", validators=[DataRequired(), Length(2, 48)])
    last_name = StringField("Фамилия: ", validators=[DataRequired(), Length(2, 48)])
    address = StringField("Адрес: ", validators=[DataRequired(), Length(2, 48)])
    passport_data = StringField("Паспортные данные: ", validators=[DataRequired(), Length(2, 48)])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    password2 = PasswordField("Пароль еще раз: ", validators=[DataRequired(), EqualTo("password", 
        message="Пароли должны совпадать")])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    phone = StringField("Номер телефона: ", validators=[DataRequired()])
    gender = SelectField('Пол', choices=["М", "Ж"])
    date = DateField('Дата рождения', validators=[DataRequired()], format='%m.%d.%Y')

    submit = SubmitField("Регистрация")

    def validate_username(self, field):
        if get_user(field.data):
            raise ValidationError("Username already exists")

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
