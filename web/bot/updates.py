from flask import json
from web.bot import users
from threading import currentThread
from time import localtime


def check_and_decode_json(update_json):
    updates = json.JSONDecoder().decode(update_json)
    if updates['ok']:
        result = take_messages_from_updates(updates['result'])
    else:
        result = None
    return result


def take_messages_from_updates(updates):
    messages = []
    for update in updates:
        if update.get('message') is not None:
            message = Message(update)
            messages.append(message)
    return messages


class Message:
    def __init__(self, update=None, message=None):
        if update is not None:
            message = update['message']

            self.upd_id = update['update_id']
            self.msg_id = message['message_id']
            self.user = users.DefUser(message['from'])
            self.chat_id = message['chat']['id']
            self.text = update['message'].get('text')
        elif message is not None:
            self.upd_id = message['upd_id']
            self.msg_id = message['msg_id']
            self.user = users.DefUser(message['user'])
            self.chat_id = message['chat_id']
            self.text = message['text']

    def message_response(self):
        if self.user.valid and self.text is not None:
            txt = self.text.lower()
            if txt == '/time':
                time = localtime()
                time_str = '{time[3]:0>2}:{time[4]:0>2}'.format(time=time)
                answer = "My time is "+time_str
            elif txt == '/date':
                date = localtime()
                date_str = '{date[2]:0>2}.{date[1]:0>2}.{date[0]:0>4}'.format(date=date)
                answer = "My date is "+date_str
            elif txt == '/start':
                answer = "Hello. I'm ready for working."
            elif txt == '/stop':
                answer = "Turning off"
                currentThread().is_active = False
            else:
                answer = "I don't understand"
        elif self.text is None:
            answer = 'What is it?'
        else:
            answer = "You're not registered yet. Try contacting my Administrator (@unwado)."
        response = {
            'chat_id': self.chat_id,
            'text': answer
        }
        return response

    def to_dict(self):
        dictionary = {
            'upd_id': self.upd_id,
            'msg_id': self.msg_id,
            'user': self.user.to_dict(),
            'chat_id': self.chat_id,
            'text': self.text

        }
        return dictionary
