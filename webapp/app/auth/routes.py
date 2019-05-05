from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, is_active=True).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username o password non validi')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        numUtenti=User.query.count()
        if numUtenti < 1:
            user = User(username=form.username.data, email=form.email.data, cellular=form.cellular.data, is_admin=True, is_active=True)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        else: 
            user = User(username=form.username.data, email=form.email.data, cellular=form.cellular.data, is_admin=False, is_active=False)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            admin = User.query.filter_by(is_admin=True).first()
            admin.add_notification('registration_request', admin.new_requests())
            db.session.commit()
        flash('Congratulazioni, ora sei un utente registrato!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Registrazione', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Controlla la tua casella email per conoscere le istruzione per il reset della password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('La tua password è stata resettata.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)