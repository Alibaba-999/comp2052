from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Role',
        choices=[('Lector', 'Lector'), ('Moderador', 'Moderador'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un curso
class LibroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    anio_publicacion = IntegerField('Año de Publicación', validators=[Optional()])
    genero = StringField('Género', validators=[Optional(), Length(max=50)])
    url = URLField('URL', validators=[Optional(), URL()])
    notas = TextAreaField('Notas', validators=[Optional()])
    etiquetas = StringField('Etiquetas', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Guardar')
