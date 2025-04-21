from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class TransaccionForm(FlaskForm):
    monto = FloatField('Monto', validators=[DataRequired()])
    categoria = SelectField(
        'Categoría',
        choices=[
            ('salario', 'Salario'),
            ('regalos', 'Regalos'),
            ('intereses', 'Intereses'),
            ('inversiones', 'Inversiones'),
            ('otros', 'Otros'),
            ('alquiler', 'Alquiler'),
            ('alimentos', 'Alimentos'),
            ('transporte', 'Transporte'),
            ('entretenimiento', 'Entretenimiento'),
            ('ropa', 'Ropa'),
            ('salud', 'Salud'),
        ],
        validators=[DataRequired()]
    )
    tipo = SelectField(
        'Tipo',
        choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Registrar')

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')