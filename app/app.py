import os

from flask import Flask, render_template, redirect
from flask import flash
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from forms import SignupForm, LoginForm, AddGameForm

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

# This has to be after db creation for alembic to work properly
import models

CURRENT_USER_ID = 'current_user'


@app.before_request
def before_request():
    if CURRENT_USER_ID not in session and request.endpoint not in ['login', 'signup']:
        flash('You need to login first')
        return redirect(url_for('login'))


@app.teardown_request
def teardown_request(exception):
    if exception:
        app.logger.error("An error occured, rolling back session as a precaution: {}".format(exception))
        models.db.session.rollback()


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/users')
def users():
    return list_table(models.User)


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = models.User.query.get(user_id)
    return render_template('user.html', user=user)


@app.route('/players')
def players():
    return render_template('users.html', users=models.User.query.all())


@app.route('/games', methods=['GET', 'POST'])
def games():
    form = AddGameForm(request.form)
    if request.method == 'POST' and form.validate():
        if models.Game.query.filter_by(name=form.game_name.data.lower()).first():
            flash('Game already exists')
        else:
            game = models.Game(form.game_name.data)
            models.db.session.add(game)
            models.db.session.commit()
        return redirect(url_for('games'))
    return render_template('games.html', games=models.Game.query.all(), form=form)


@app.route('/config')
def config():
    config = ""
    for key, value in app.config.items():
        config += "<div>"
        config += "{}: {}".format(key, value)
        config += "</div>"
    return config


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        if models.User.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already exists')
            return redirect(url_for('signup'))
        user = models.User(form.username.data, form.email.data,
                           form.password.data)
        models.db.session.add(user)
        models.db.session.commit()
        app.logger.debug("New user: {}".format(user))
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, title='Sign up')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if CURRENT_USER_ID in session:
        user_id = session[CURRENT_USER_ID]
        app.logger.debug('User with id {} found'.format(user_id))
        return redirect(url_for('user_profile', user_id=user_id))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('Log in successful')
            session[CURRENT_USER_ID] = user.id
            return redirect(url_for('user_profile', user_id=user.id))
        else:
            flash('Bad username or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    session.pop('current_user')
    return redirect(url_for('login'))


@app.route("/go", methods=['GET', 'POST'])
def go():
    if request.method == 'POST':
        champion_name = request.form['champion']
        champion = models.Player.query.filter_by(username=champion_name).first()
        go = models.Game.query.filter_by(name='go').first()
        go.champion_id = champion.id
        models.db.session.commit()
        app.logger.debug("New champion: {}".format(champion_name))
    else:
        go = models.Game.query.filter_by(name='go').first()
        try:
            champion_name = go.champion.username
        except AttributeError:
            champion_name = 'Personne'

    return render_template('go.html', name=champion_name)


def list_table(model):
    html = ""
    entries = model.query.all()
    for entry in entries:
        html += "<div>{}</div>".format(entry)
    return html


if __name__ == "__main__":
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)
