"""
    server.py - OpenREC API
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/22/18
"""

from flask import Flask, jsonify, render_template

from worker import Worker
from open_rec import OpenREC

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
    rec = OpenREC()
    top_recommendations = rec.get_top_recommendations(0, number, 3)

    response = {
        'header': 'User {}\'s profile'.format(number),
        'top_recommendations': top_recommendations
    }
    return render_template('user.html', data=response)


if __name__ == '__main__':
    app.run()
