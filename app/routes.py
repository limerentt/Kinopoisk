from lib2to3.pytree import generate_matches
from app import app, db
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask import render_template, redirect, session, url_for, request
from app.forms import LoginForm, RegistrationForm, FilterForm
from app.models import Film, User, Genre, Person, DirectorShip, GenreShip, CharacterShip
from app.template_classes.classes import ImpFilm, generate_impfilms


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    filterform = FilterForm()
    filter_films = [film for film in Film.query.order_by(Film.date.desc())]
    if filterform.validate_on_submit():
        if filterform.genre.data != "":
            genre = Genre.query.get(int(filterform.genre.data))
            select_films = [genreship.film for genreship in GenreShip.query.filter_by(genre=genre)]
            iter = list(filter_films)
            for film in iter:
                if film not in select_films:
                    filter_films.remove(film)
        if filterform.director.data != "":
            director = Person.query.get(int(filterform.director.data))
            select_films = [directorship.film for directorship in DirectorShip.query.filter_by(director=director)]
            iter = list(filter_films)
            for film in iter:
                if film not in select_films:
                    filter_films.remove(film)
        if filterform.character.data != "":
            character = Person.query.get(int(filterform.character.data))
            select_films = [charactership.film for charactership in CharacterShip.query.filter_by(character=character)]
            iter = list(filter_films)
            for film in iter:
                if film not in select_films:
                    filter_films.remove(film)
        
    print(filter_films)
    films = generate_impfilms(filter_films)
    
    return render_template('index.html', films=films, filterform=filterform, count=4)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/film_view/<_film>', methods=['GET', 'POST'])
@login_required
def film_view(_film):
    film = generate_impfilms([Film.query.get(int(_film))])[0][0]
    return render_template('film_view.html', film=film)


@app.route('/profile/<_user>', methods=['GET', 'POST'])
@login_required
def profile(_user):
    user = User.query.get(int(_user))
    books = []
    return render_template('profile.html', books=books)