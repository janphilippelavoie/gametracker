import os

from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

# This has to be after db creation for alembic to work properly
import models


@app.route('/')
def root():
    return redirect(url_for(go.__name__))


@app.route('/players')
def list_players():
    return list_table(models.Player)


@app.route('/games')
def list_games():
    return list_table(models.Game)


@app.route('/config')
def config():
    config = ""
    for key, value in app.config.items():
        config += "<div>"
        config += "{}: {}".format(key, value)
        config += "</div>"
    return config


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
