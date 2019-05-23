from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Su di me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Modifica')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Utilizza uno username differente.')

# Da rimuovere (Solo per prova)
class PostForm(FlaskForm):
    post = TextAreaField('Racconta qualcosa', validators=[DataRequired()])
    submit = SubmitField('Invia')

# Da rimuovere (Solo per prova)
class MessageForm(FlaskForm):
    message = TextAreaField('Messaggio', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Invia')

class PianoForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Descrizione', validators=[DataRequired()])
    submit = SubmitField('Crea')

class StanzaForm(FlaskForm):
    piano = SelectField('Piano:', coerce=int, validators=[DataRequired()], id='select_piano')
    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Descrizione', validators=[DataRequired()])
    submit = SubmitField('Crea')

class DispositivoForm(FlaskForm):
    piano = SelectField('Piano:', coerce=int, validators=[DataRequired()], id='select_piano')
    stanza = SelectField('Stanza:', coerce=int, validators=[DataRequired()], id='select_stanza')
    tipo = SelectField('Tipologia:', coerce=int, validators=[DataRequired()], id='select_dispositivo')
    pin = StringField('Pin:', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Descrizione', validators=[DataRequired()])
    submit = SubmitField('Crea')

class PulsanteForm(FlaskForm):
    piano = SelectField('Piano:', coerce=int, validators=[DataRequired()], id='select_piano')
    stanza = SelectField('Stanza:', coerce=int, validators=[DataRequired()], id='select_stanza')
    topic = SelectField('Topic', coerce=int, validators=[DataRequired()], id='select_topic')
    pin = StringField('Pin:', validators=[DataRequired()])
    description = StringField('Descrizione', validators=[DataRequired()])
    submit = SubmitField('Crea')

class RiscaldamentoForm(FlaskForm):
    piano = SelectField('Piano:', coerce=int, validators=[DataRequired()], id='select_piano')
    stanza = SelectField('Stanza:', coerce=int, validators=[DataRequired()], id='select_stanza')
    temperatura = IntegerField('Temperatura:', validators=[DataRequired()])
    orario = DateTimeLocalField('Orario', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Imposta')