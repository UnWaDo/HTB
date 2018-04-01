from config import ALLOWED_USERS as AL_US


class DefUser:
    def __init__(self, user):
        self.last_name = user.get('last_name')
        self.first_name = user.get('first_name')
        self.id = user['id']
        self.valid = self.id in AL_US

    def to_dict(self):
        dictionary = {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'id': self.id
        }
        return dictionary

