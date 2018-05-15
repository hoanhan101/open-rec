"""
    server.py - OpenREC Server
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/22/18
"""

import threading

from flask import Flask, jsonify, render_template
from time import ctime, time

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

@app.route('/test', methods=['GET'])
def test():
    """
    Test endpoint
    """
    response = {
        'status': 'ok',
        'timestamp': ctime(time())
    }
    return jsonify(response)

@app.route('/config', methods=['GET'])
def config():
    """
    Return configurations. 
    """
    response = {
        'rating_path': RATINGS_PATH,
        'movie_path': MOVIES_PATH,
        'nums_recommendations': NUMS_RECOMMENDATIONS,
        'matrix_factorization': {
            'debug': MF_DEBUG,
            'steps': MF_STEPS,
            'gamma': MF_GAMMA,
            'lamda': MF_LAMDA
        },
        'nums_worker': NUMS_WORKERS,
        'min_id': MIN_ID,
        'max_id': MAX_ID
    }

    return jsonify(response) 

@app.route('/user/<int:user_id>/data', methods=['GET'])
def find_data(user_id):
    """
    Return user's data in JSON.
    """
    presenter = Presenter(user_id)

    response = {
        'user_id': user_id,
        'top_favorites': presenter.get_data('TF'),
        'nearest_neighbours': presenter.get_data('NN'),
        'latent_factors': presenter.get_data('LF') 
    }

    return jsonify(response) 

@app.route('/user/<int:user_id>/poster', methods=['GET'])
def find_poster_raw(user_id):
    """
    Return User's Profile in JSON.
    """
    presenter = Presenter(user_id)

    response = {
        'user_id': user_id,
        'top_favorites': presenter.get_posters('TF', 8),
        'nearest_neighbours': presenter.get_posters('NN', 8),
        'latent_factors': presenter.get_posters('LF', 8) 
    }

    return jsonify(response) 

@app.route('/user/<int:user_id>/view', methods=['GET'])
def find_poster(user_id):
    """
    User's Profile Page.
    """
    presenter = Presenter(user_id)

    response = {
        'header': 'OpenREC',
        'user_id': user_id,
        'top_favorites': presenter.get_posters('TF', 8),
        'nearest_neighbours': presenter.get_posters('NN', 8),
        'latent_factors': presenter.get_posters('LF', 8) 
    }

    return render_template('user.html', data=response)


if __name__ == '__main__':
    app.run()
