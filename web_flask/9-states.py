#!/usr/bin/python3
"""
    script that starts a Flask web application
"""
from flask import Flask, render_template, template_rendered
from models import storage
from models.state import State
from models.city import City
from models.engine.db_storage import DBStorage

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/states')
@app.route('/states/<id>')
def display_states(id=None):
    """
    Route
    """
    states = storage.all(State)
    cities = storage.all(City)
    return render_template('9-states.html', states = states, cities = cities, id = id)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    close session
    """
    storage.close()

if __name__ == "__main__":
    app.run(
        host  = "0.0.0.0",
        port=5000
    )
