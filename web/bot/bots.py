import logging

import requests
from flask import json

from web.bot.updates import check_and_decode_json, Message


class SendingError(BaseException):
    pass


class ControlBot:

    def __init__(self, token=None, url=None, updates=None, last_upd_id=None):
        if token is not None:
            self.url = 'https://api.telegram.org/bot' + token + '/'
            self.updates = []
            self.last_update_id = 0
        elif (url, updates, last_upd_id) is not None:
            self.url = url
            self.updates = updates
            self.last_update_id = last_upd_id

    def load_updates(self):
        payload = {
            'offset': self.last_update_id,
            'allowed_updates': 'message',
            'timeout': 1000
        }
        try:
            response = requests.post(self.url+'getUpdates', json=payload)
            self.updates = check_and_decode_json(response.content.decode('utf-8'))
            if self.updates:
                self.updates = sorted(self.updates, key=lambda update: update.upd_id)
                self.last_update_id = self.updates[-1].upd_id + 1

        except requests.ConnectionError:
            logging.error('Connection error (loading updates)', filename='log.txt')
            raise ConnectionError

    def send_message(self, message):
        data = message.message_response()
        try:
            status = requests.post(self.url+"sendMessage", json=data)
            decoded_status = json.JSONDecoder().decode(status.content.decode('utf-8'))
            if not decoded_status.get('ok'):
                logging.error('Sending error', filename='log.txt')
                raise SendingError
        except requests.ConnectionError:
            logging.error('Connection error (loading updates)', filename='log.txt')
            raise ConnectionError

    def to_json(self):
        updates = []
        if self.updates:
            for update in self.updates:
                updates.append(update.to_dict())
        coded = json.dumps({
            'url': self.url,
            'last_upd_id': self.last_update_id,
            'updates': updates
        })

        return coded

    def save_bot(self):
        jsoned_bot = self.to_json()
        f = open('web/bot.txt', 'w')
        f.write(jsoned_bot)
        f.close()


def create_bot_from_json(json_str):
    decoded = json.JSONDecoder().decode(json_str)
    url = decoded['url']
    updates = [Message(message=upd) for upd in decoded['updates']]
    last_upd_id = decoded['last_upd_id']

    return ControlBot(url=url, updates=updates, last_upd_id=last_upd_id)


