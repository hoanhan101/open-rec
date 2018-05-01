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


@app.route('/user/<int:number>', methods=['GET'])
def find(number):
    """
    User's Profile Page.
    """
    presenter = Presenter(number)

    response = {
        'header': 'User {}\'s profile'.format(number),
        'top_favorites': presenter.get_TF_data(),
        'nearest_neighbours': presenter.get_NN_data(),
        'latent_factors': presenter.get_LF_data() 
    }

    return render_template('user.html', data=response)


if __name__ == '__main__':
    app.run()
