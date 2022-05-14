#!/usr/bin/python3
"""
    script that starts a Flask web application
"""
from os import stat_result
from flask import Flask, render_template, template_rendered
from models import storage
from models.state import State
from models.engine.db_storage import DBStorage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def display_states():
    """
    Route
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    close session
    """
    storage.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
