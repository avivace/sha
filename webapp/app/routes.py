from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, PianoForm, StanzaForm, DispositivoForm, MessageForm, PulsanteForm
from app.models import User, Post, Piano, Stanza, Attuatore, Sensore, Message, Notification, Pulsante
from app.email import send_password_reset_email
import paho.mqtt.client as mqtt

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, is_active=True).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/user_not_active')
@login_required
def user_not_active():
    if current_user.is_admin:
        userNotActive = User.query.filter_by(is_active=False).all()
        return render_template('user_not_active.html', users=userNotActive)
    else:
        return render_template('404.html')

@app.route('/accept_user/<username>')
@login_required
def accept_user(username):
    if current_user.is_admin:
        user = User.query.filter_by(username=username, is_active=False).first()
        if user is None:
            return jsonify(message='Username errato o mancante')
        else:
            user.is_active=True
            db.session.commit()
            current_user.add_notification('registration_request', current_user.new_requests())
            db.session.commit()
            return jsonify(message='Utente accettato')

@app.route('/reject_user/<username>')
@login_required
def reject_user(username):
    if current_user.is_admin:
        User.query.filter_by(username=username, is_active=False).delete()
        db.session.commit()
        current_user.add_notification('registration_request', current_user.new_requests())
        db.session.commit()
        return jsonify(message='Utente rimosso')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)

@app.route('/aggiungi_piano', methods=['GET', 'POST'])
@login_required
def aggiungi_piano():
    form = PianoForm()
    if form.validate_on_submit():
        topic = Piano.query.filter_by(topic=form.topic.data).first()
        if topic is None:
            piano = Piano(topic=form.topic.data, description=form.description.data)
            db.session.add(piano)
            db.session.commit()
            flash('Congratulazioni, Piano registrato correttamente')
            return redirect(url_for('index'))
        flash('Topic gia esistente')
        return redirect(url_for('aggiungi_piano'))
    return render_template('aggiungi_piano.html', title='Aggiungi Piano', form=form)

@app.route('/aggiungi_stanza', methods=['GET', 'POST'])
@login_required
def aggiungi_stanza():
    form = StanzaForm()
    form.piano.choices = [(row.id, row.description) for row in Piano.query.all()]
    if form.validate_on_submit():
        topic = Stanza.query.filter_by(topic=form.topic.data, piano_id=form.piano.data).first()
        if topic is None:
            stanza = Stanza(topic=form.topic.data, description=form.description.data, piano_id=form.piano.data)
            db.session.add(stanza)
            db.session.commit()
            flash('Congratulazioni, Stanza registrata correttamente')
            return redirect(url_for('index'))
        flash('Topic gia esistente')
        return redirect(url_for('aggiungi_stanza'))
    return render_template('aggiungi_stanza.html', title='Aggiungi Stanza', form=form)

@app.route('/aggiungi_dispositivo', methods=['GET', 'POST'])
@login_required
def aggiungi_dispositivo():
    form = DispositivoForm()
    form.piano.choices = [(row.id, row.description) for row in Piano.query.all()]
    form.stanza.choices = [(row.id, row.description) for row in Stanza.query.all()]
    form.tipo.choices = [(1,'Lampada'),(2,'Termostato'), (3,'Serratura'), (4,'Sensore')]
    if form.validate_on_submit():
        if form.tipo.data == 1:
            topic = Attuatore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Attuatore(topic=form.topic.data, description=form.description.data, type='lampada', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, lampada registrata correttamente')
                return redirect(url_for('index'))
        elif form.tipo.data == 2:
            topic = Attuatore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Attuatore(topic=form.topic.data, description=form.description.data, type='termostato', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, termostato registrato correttamente')
                return redirect(url_for('index'))
        elif form.tipo.data == 3:
            topic = Attuatore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Attuatore(topic=form.topic.data, description=form.description.data, type='serratura', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, serratura registrata correttamente')
                return redirect(url_for('index'))
        elif form.tipo.data == 4:
            topic = Sensore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Sensore(topic=form.topic.data, description=form.description.data, type='temperatura', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, sensore registrato correttamente')
                return redirect(url_for('index'))
        flash('Topic gia esistente')
        return redirect(url_for('aggiungi_dispositivo'))
    return render_template('aggiungi_dispositivo.html', title='Aggiungi Dispositivo', form=form)

# Restituisce l'elenco di tutti i topic associati ad attuatori di tipo lampada
def get_topics():
    piani = Piano.query.all()
    topicArray = []

    for piano in piani:
        stanze = Stanza.query.filter_by(piano_id=piano.id).all()
        for stanza in stanze:
        # Aggiungere elenco attuatori sia di tipo "lampada" che di tipo "serratura"
        # Da vedere come costruire la query con operatore di OR
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id, type='lampada')
            for attuatore in attuatori:
                topicObj = {}
                topicObj['id'] = attuatore.id
                topicObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
            topicArray.append(topicObj)

    return topicArray

@app.route('/aggiungi_pulsante', methods=['GET', 'POST'])
@login_required
def aggiungi_pulsante():
    topics = get_topics()
    form = PulsanteForm()
    form.piano.choices = [(row.id, row.description) for row in Piano.query.all()]
    form.stanza.choices = [(row.id, row.description) for row in Stanza.query.all()]
    form.topic.choices = [(row['id'], row['topic']) for row in topics]
    if form.validate_on_submit():
        pulsante = Pulsante(attuatore_id=form.topic.data, description=form.description.data, pin=form.pin.data, stanza_id=form.stanza.data)
        db.session.add(pulsante)
        db.session.commit()
        flash('Congratulazioni, pulsante registrato correttamente')
        return redirect(url_for('index'))
    return render_template('aggiungi_pulsante.html', title='Aggiungi Pulsante', form=form)

# Recupera la struttura dell'abitazione per poi far costruire l'interfaccia di controllo
@app.route('/dashboard')
@login_required
def dashboard():
    piani = Piano.query.all()

    pianiArray = []
    stanzeArray = []
    attuatoriArray = []

    for piano in piani:
        pianoObj = {}
        pianoObj['id'] = piano.id
        pianoObj['description'] = piano.description
        stanze = Stanza.query.filter_by(piano_id=piano.id).all()
        for stanza in stanze:
            stanzaObj = {}
            stanzaObj['id'] = stanza.id
            stanzaObj['description'] = stanza.description
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id, type='lampada')
            for attuatore in attuatori:
                attuatoreObj = {}
                attuatoreObj['id'] = attuatore.id
                attuatoreObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
                attuatoreObj['description'] = attuatore.description
                attuatoriArray.append(attuatoreObj)
            stanzaObj['attuatori'] = attuatoriArray
            stanzeArray.append(stanzaObj)
            attuatoriArray = []
        pianoObj['stanze'] = stanzeArray
        pianiArray.append(pianoObj)
        stanzeArray = []

    return render_template('dashboard.html', piani=pianiArray)

# Restituisce l'elenco delle stanze di un determinato piano
@app.route('/stanza/<pianoId>')
@login_required
def stanza(pianoId):
    stanze = Stanza.query.filter_by(piano_id=pianoId).all()
    stanzaArray = []

    for stanza in stanze:
        stanzaObj = {}
        stanzaObj['id'] = stanza.id
        stanzaObj['description'] = stanza.description
        stanzaArray.append(stanzaObj)

    return jsonify({'stanze' : stanzaArray})

# Restituisce l'elenco dei topic appartenenti alla coppia Piano-Stanza
@app.route('/topic/<pianoId>/<stanzaId>')
@login_required
def topic(pianoId, stanzaId):
    piani = Piano.query.filter_by(id=pianoId)
    topicArray = []

    for piano in piani:
        stanze = Stanza.query.filter_by(piano_id=pianoId, id=stanzaId)
        for stanza in stanze:
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id, type='lampada')
            for attuatore in attuatori:
                topicObj = {}
                topicObj['id'] = attuatore.id
                topicObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
            topicArray.append(topicObj)

    return jsonify({'topics' : topicArray})

# Effettua Publish MQTT per far attuare al backend i comandi sugli attuatori
@app.route('/attuatore/<piano_topic>/<stanza_topic>/<attuatore_topic>/<value>')
@login_required
def attuatore(piano_topic, stanza_topic, attuatore_topic, value):
    try:
        client = mqtt.Client()
        client.connect("192.168.1.14", 1883, 60)
        topic = "notifica/controlloreInterfaccia"
        client.publish(topic, "OK")
    except:
        print("ERRORE MQTT")
        return jsonify(message='Errore')

    client.connect("192.168.1.14", 1883, 60)
    topic = piano_topic + '/' + stanza_topic + '/' + attuatore_topic
    client.publish(topic, value)

    return jsonify(message='Azione eseguita')