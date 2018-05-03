"""
    server.py - OpenREC Server
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/22/18
"""

import threading

from flask import Flask, jsonify, render_template

from presenter import Presenter
from config import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    """
    Landing page.
    """
    response = {
        'header': 'Welcome to OpenREC!',
    }
    return render_template('landing.html', data=response)


@app.route('/user/<int:user_id>', methods=['GET'])
def find(user_id):
    """
    User's Profile Page.
    """
    presenter = Presenter(user_id)

    response = {
        'header': 'OpenREC'.format(user_id),
        'top_favorites': presenter.get_posters('TF', 8),
        'nearest_neighbours': presenter.get_posters('NN', 8),
        'latent_factors': presenter.get_posters('LF', 8) 
    }

    return render_template('user.html', data=response)


if __name__ == '__main__':
    app.run()
