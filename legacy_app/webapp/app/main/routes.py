from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm, EditProfileForm, \
    PianoForm, StanzaForm, DispositivoForm, MessageForm, PulsanteForm, RiscaldamentoForm
from app.models import User, Post, Piano, Stanza, Attuatore, Sensore, Message, Notification, Pulsante, Riscaldamento
from app.main import bp
import paho.mqtt.client as mqtt

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Il tuo post è stato pubblicato !')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Le modifiche sono state salvate.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Modifica profilo', form=form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Utente {} non trovato.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Non puoi essere follower di te stesso !')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Stai seguendo {}!'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Utente {} non trovato.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Non puoi non essere follower di te stesso !')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Non segui più {}.'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/notifications')
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

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Il tuo messaggio è stato inviato.')
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title='Invia messaggio',
                           form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)

@bp.route('/user_not_active')
@login_required
def user_not_active():
    if current_user.is_admin:
        userNotActive = User.query.filter_by(is_active=False).all()
        return render_template('user_not_active.html', users=userNotActive)
    else:
        return render_template('errors/404.html')

@bp.route('/accept_user/<username>')
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

@bp.route('/reject_user/<username>')
@login_required
def reject_user(username):
    if current_user.is_admin:
        User.query.filter_by(username=username, is_active=False).delete()
        db.session.commit()
        current_user.add_notification('registration_request', current_user.new_requests())
        db.session.commit()
        return jsonify(message='Utente rimosso')

@bp.route('/aggiungi_piano', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))
        flash('Topic gia esistente')
        return redirect(url_for('main.aggiungi_piano'))
    return render_template('aggiungi_piano.html', title='Aggiungi Piano', form=form)

@bp.route('/aggiungi_stanza', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))
        flash('Topic gia esistente')
        return redirect(url_for('main.aggiungi_stanza'))
    return render_template('aggiungi_stanza.html', title='Aggiungi Stanza', form=form)

@bp.route('/aggiungi_dispositivo', methods=['GET', 'POST'])
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
                return redirect(url_for('main.index'))
        elif form.tipo.data == 2:
            topic = Attuatore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Attuatore(topic=form.topic.data, description=form.description.data, type='termostato', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, termostato registrato correttamente')
                return redirect(url_for('main.index'))
        elif form.tipo.data == 3:
            topic = Attuatore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Attuatore(topic=form.topic.data, description=form.description.data, type='serratura', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, serratura registrata correttamente')
                return redirect(url_for('main.index'))
        elif form.tipo.data == 4:
            topic = Sensore.query.filter_by(stanza_id=form.stanza.data, topic=form.topic.data).first()
            if topic is None:
                dispositivo = Sensore(topic=form.topic.data, description=form.description.data, type='temperatura', pin=form.pin.data, stanza_id=form.stanza.data)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Congratulazioni, sensore registrato correttamente')
                return redirect(url_for('main.index'))
        flash('Topic gia esistente')
        return redirect(url_for('main.aggiungi_dispositivo'))
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

@bp.route('/aggiungi_pulsante', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('aggiungi_pulsante.html', title='Aggiungi Pulsante', form=form)

# Recupera la struttura dell'abitazione per poi far costruire l'interfaccia di controllo
@bp.route('/dashboard/<tipologia>')
@login_required
def dashboard(tipologia):
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
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id, type=tipologia)
            for attuatore in attuatori:
                attuatoreObj = {}
                attuatoreObj['id'] = attuatore.id
                attuatoreObj['type'] = attuatore.type
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
@bp.route('/stanza/<pianoId>')
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
@bp.route('/topic/<pianoId>/<stanzaId>')
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
@bp.route('/attuatore/<piano_topic>/<stanza_topic>/<attuatore_topic>/<value>')
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

@bp.route('/riscaldamento/<attuatore_id>', methods=['GET', 'POST'])
@login_required
def riscaldamento(attuatore_id):
    form = RiscaldamentoForm()
    termostato = Attuatore.query.filter_by(id=attuatore_id).first()
    stanza_id = termostato.stanza_id
    stanza = Stanza.query.filter_by(id = stanza_id).first()
    piano_id = stanza.piano_id
    piano = Piano.query.filter_by(id=piano_id).first()
    form.piano.choices = [(row.id, row.description) for row in Piano.query.filter_by(id=piano_id)]
    form.stanza.choices = [(row.id, row.description) for row in Stanza.query.filter_by(id=stanza_id)]
    if form.validate_on_submit():
        riscaldamento = Riscaldamento(set_temperatura=form.temperatura.data, set_orario=form.orario.data, attuatore_id=attuatore_id)
        db.session.add(riscaldamento)
        db.session.commit()
        try:
            client = mqtt.Client()
            client.connect("192.168.1.14", 1883, 60)
            topic = "notifica/controlloreInterfaccia"
            client.publish(topic, "OK")
        except:
            print("ERRORE MQTT")

        client.connect("192.168.1.14", 1883, 60)
        topic = piano.topic + '/' + stanza.topic + '/' + termostato.topic
        client.publish(topic, 0)
        flash('Congratulazioni, attività di riscaldamento registrata correttamente')
        return redirect(url_for('main.index'))
    return render_template('riscaldamento.html', title='Riscaldamento', form=form)