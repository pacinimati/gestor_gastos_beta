from flask import render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import TransaccionForm, RegistroForm, LoginForm
from app.models import Transaccion, Usuario
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    # Filtrar transacciones del usuario actual
    transacciones_usuario = Transaccion.query.filter_by(usuario_id=current_user.id).all()

    # Calcular totales de ingresos y egresos
    total_ingresos = sum(t.monto for t in transacciones_usuario if t.tipo == 'ingreso')
    total_egresos = sum(t.monto for t in transacciones_usuario if t.tipo == 'egreso')

    # Agrupar por categorías
    ingresos = [t for t in transacciones_usuario if t.tipo == 'ingreso']
    egresos = [t for t in transacciones_usuario if t.tipo == 'egreso']

    ingresos_categorias = list(set(t.categoria for t in ingresos))
    ingresos_valores = [sum(t.monto for t in ingresos if t.categoria == cat) for cat in ingresos_categorias]

    egresos_categorias = list(set(t.categoria for t in egresos))
    egresos_valores = [sum(t.monto for t in egresos if t.categoria == cat) for cat in egresos_categorias]

    return render_template(
        'index.html',
        total_ingresos=total_ingresos,
        total_egresos=total_egresos,
        ingresos_categorias=ingresos_categorias,
        ingresos_valores=ingresos_valores,
        egresos_categorias=egresos_categorias,
        egresos_valores=egresos_valores,
        transacciones=transacciones_usuario,  # Solo transacciones del usuario actual
        zip=zip
    )

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data  # Contraseña sin encriptar
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            if usuario.password == form.password.data:  # Comparar contraseñas directamente
                login_user(usuario)
                flash('Inicio de sesión exitoso.')
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta.')
        else:
            flash('Correo no encontrado.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

@app.route('/transaccion', methods=['GET', 'POST'])
@login_required
def transaccion():
    form = TransaccionForm()
    if form.validate_on_submit():
        transaccion = Transaccion(
            monto=form.monto.data,
            categoria=form.categoria.data,
            tipo=form.tipo.data,
            fecha=datetime.utcnow(),
            usuario_id=current_user.id  # Usar el ID del usuario autenticado
        )
        db.session.add(transaccion)
        db.session.commit()
        flash('Transacción registrada con éxito.')
        return redirect(url_for('transaccion'))
    return render_template('transaccion.html', form=form)