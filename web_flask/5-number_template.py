#!/usr/bin/python3
"""
    script that starts a Flask web application
"""
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbhb():
    """
    function returns just a text
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hello_hbnb2():
    """
    function returns just a text
    """
    return "HBNB"


@app.route('/c/<text>')
def hello_hbnb3(text):
    """
    function returns just a text
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python')
@app.route('/python/<text>')
def hello_hbnb4(text='is cool'):
    """
    function returns just a text
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number_template/<int:n>')
def hello_hbnb5(n):
    """
    function displays a HTML page only if n is an integer
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
