from unicodedata import name
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Film(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    date = db.Column(db.Integer, index=True)
    path = db.Column(db.Text)

    def __repr__(self):
        return self.title


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return self.name


class GenreShip(db.Model):
    __tablename__ = 'genreships'
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    film = db.relationship(Film, backref=db.backref("genreships", cascade="all, delete-orphan"))
    genre = db.relationship(Genre, backref=db.backref("genreships", cascade="all, delete-orphan"))

    def __repr__(self):
        return "{}->{}".format(self.film, self.genre)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    surename = db.Column(db.String(64), index=True)

    def __repr__(self):
        return "{} {}".format(self.name, self.surename)


class DirectorShip(db.Model):
    __tablename__ = 'directorships'
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    film = db.relationship(Film, backref=db.backref("directorships", cascade="all, delete-orphan"))
    director = db.relationship(Person, backref=db.backref("directorships", cascade="all, delete-orphan"))

    def __repr__(self):
        return "{}->{}".format(self.film, self.director)


class CharacterShip(db.Model):
    __tablename__ = 'characterships'
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    film = db.relationship(Film, backref=db.backref("characterships", cascade="all, delete-orphan"))
    character = db.relationship(Person, backref=db.backref("characterships", cascade="all, delete-orphan"))

    def __repr__(self):
        return "{}->{}".format(self.film, self.character)
