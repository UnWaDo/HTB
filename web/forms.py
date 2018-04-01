from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, SelectField
from config import ALLOWED_USERS as AL_US


class BotStartForm(FlaskForm):
    token_field = StringField('Token')
    is_new_field = BooleanField('Is new?')
    submit = SubmitField('Start bot')


class BotStopForm(FlaskForm):
    stop = SubmitField('Stop bot')


class BotAddUserForm(FlaskForm):
    user_id_field = IntegerField('User id')
    submit = SubmitField('Add id')


class BotRemoveUserForm(FlaskForm):
    user_id_field = SelectField('Select user to delete', choices=AL_US)
    submit = SubmitField('Remove id')

