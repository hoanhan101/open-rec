"""
    server.py - OpenREC API
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/22/18
"""

import threading

from flask import Flask, jsonify, render_template

from worker import Worker
from open_rec import OpenREC
from config import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    """
    Test endpoint.
    """
    response = {
        'header': 'Welcome to OpenREC!',
    }
    return render_template('landing.html', data=response)


@app.route('/user/<int:number>', methods=['GET'])
def find(number):
    """
    TODO
    """
    threads = []

    worker_TF = Worker(thread_id=0,
                       task='top_favorites',
                       user_id=number,
                       limit=NUMS_RECOMMENDATIONS)

    worker_NN = Worker(thread_id=1,
                       task='nearest_neighbours',
                       user_id=number,
                       limit=NUMS_RECOMMENDATIONS)

    worker_LT = Worker(thread_id=2, 
                       task='latent_factors',
                       user_id=number, 
                       limit=NUMS_RECOMMENDATIONS)

    worker_CC = Worker(thread_id=3,
                       task='collisions',
                       user_id=number,
                       limit=NUMS_RECOMMENDATIONS)

    worker_TF.start()
    worker_NN.start()
    worker_LT.start()
    worker_CC.start()

    threads.append(worker_TF)
    threads.append(worker_NN)
    threads.append(worker_LT)
    threads.append(worker_CC)

    for t in threads:
        t.join()

    response = {
        'header': 'User {}\'s profile'.format(number),
        'top_favorites': worker_TF.data,
        'nearest_neighbours': worker_NN.data,
        'latent_factors': worker_LT.data,
        'collisions': worker_CC.data
    }

    return render_template('user.html', data=response)


if __name__ == '__main__':
    app.run()
