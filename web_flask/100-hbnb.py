#!/usr/bin/python3
"""
    script that starts a Flask web application
"""
from models import storage
from flask import Flask, render_template
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    states = storage.all(State)
    cities = storage.all(City)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template('100-hbnb.html', states=states,
                           cities=cities, amenities=amenities, places=places)


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
