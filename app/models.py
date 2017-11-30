from bcrypt import hashpw, gensalt, checkpw

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.LargeBinary())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.password = self._encrypt_password(password)

    def __repr__(self):
        return "username: {}\nemail: {}\n".format(self.username, self.email)

    def check_password(self, password):
        return checkpw(password.encode('UTF-8'), self.password)

    def reset_password(self, new_password):
        self.password = self._encrypt_password(new_password)

    @staticmethod
    def _encrypt_password(password):
        return hashpw(password.encode('UTF-8'), gensalt())


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    champion_of = db.relationship('Game', backref='champion', lazy=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return 'id {}, user {}'.format(self.id, self.username)


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    champion_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    matches = db.relationship('Match', backref='game', lazy=True)

    def __init__(self, name, champion_id=None):
        self.name = name.lower()
        self.champion_id = champion_id

    def __repr__(self):
        return 'id {}, name {}, champion: {}'.format(self.id, self.name, self.champion_id)


class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    result = db.Column(db.String())
    participants = db.relationship('User', secondary='played', backref='matches')

    def __init__(self, game_id):
        self.game_id = game_id

    def __repr__(self):
        return 'id {}, game_id {}'.format(self.id, self.game_id)


played = db.Table(
    'played',
    db.Column('match_id', db.Integer, db.ForeignKey('matches.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
