"""
    persister.py - OpenREC Persister read and write user's data to file
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 04/26/18
"""

import json

from time import gmtime, strftime
from pprint import pprint

from worker import Worker
from config import *


class Persister():
    def __init__(self, user_id):
        """
        Initialize Persister Object.

        Params:
            user_id <int>: User ID

        Return:
            None
        """
        self.user_id = user_id
        self.timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
        self.filepath = '/'.join(("output", "json", str(user_id) + ".json"))
    def read(self):
        """
        Read user's data from file.

        Params:
            None

        Return:
            data <dict>: Content of JSON file
        """
        try:
            with open(self.filepath, 'r') as raw_file:
                data = json.load(raw_file)
                return data
        except FileNotFoundError:
            data = {
                "user_id": self.user_id,
                "data": None
            }
            return data
    def write(self):
        """
        Write user's data to file.

        Params:
            None

        Return:
            data <dict>: Content of JSON file
        """
        threads = []

        worker_TF = Worker(thread_id=0,
                           task='top_favorites',
                           user_id=self.user_id,
                           limit=NUMS_RECOMMENDATIONS)

        worker_NN = Worker(thread_id=1,
                           task='nearest_neighbours',
                           user_id=self.user_id,
                           limit=NUMS_RECOMMENDATIONS)

        worker_LT = Worker(thread_id=2, 
                           task='latent_factors',
                           user_id=self.user_id, 
                           limit=NUMS_RECOMMENDATIONS)

        worker_TF.start()
        worker_NN.start()
        worker_LT.start()

        threads.append(worker_TF)
        threads.append(worker_NN)
        threads.append(worker_LT)

        for t in threads:
            t.join()

        data = {
            'user_id': self.user_id,
            'config': {
                'maxtrix_factorization': {
                    'steps': MF_STEPS,
                    'gamma': MF_GAMMA,
                    'lamda': MF_LAMDA
                },
                'worker': {
                    'nums_workers': len(threads),
                    'nums_recommendations': NUMS_RECOMMENDATIONS
                }
            },
            'data': {
                'top_favorites': worker_TF.data,
                'nearest_neighbours': worker_NN.data,
                'latent_factors': worker_LT.data
            },
            'timestamp': self.timestamp
        }

        try:
            with open(self.filepath, 'w+') as output_file:
                json.dump(data, output_file)
                return data
        except FileNotFoundError:
            data = {
                "user_id": self.user_id,
                "data": None
            }
            return data
