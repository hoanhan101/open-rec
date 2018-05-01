"""
    process_data.py - Process data
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 04/30/18
"""

import json
import requests
import urllib.parse
from pprint import pprint

from persister import Persister
from config import *


class Presenter():
    def __init__(self, user_id):
        """
        """
        self.user_id = user_id
        self.persister = Persister(self.user_id)
        self.result = self.persister.read() # init

        self.config = self.result.get('config')
        self.data = self.result.get('data')

        self.TF_data = self.data.get('top_favorites')
        self.LF_data = self.data.get('latent_factors')
        self.NN_data = self.data.get('nearest_neighbours')

    def process(self, data):
        """
        """
        endpoints = []
        for item in data:
            # Chop off unnecessary part to get a broader search result
            item = item.split('(')[0]

            # Parse URL
            query = urllib.parse.quote(item)
            endpoint = MOVIE_SEARCH_ENDPOINT + query + '&page=1'
            endpoints.append(endpoint)

        return endpoints

    def get_config(self):
        """
        """
        return self.config

    def get_TF_data(self):
        """
        """
        return self.TF_data
    
    def get_NN_data(self):
        """
        """
        return self.NN_data

    def get_LF_data(self):
        """
        """
        return self.LF_data

    def get_TF_endpoints(self):
        """
        """
        endpoints = []
        for item in self.process(self.TF_data):
            endpoints.append(item)

        return endpoints
    
    def get_TF_posters(self):
        """
        """
        posters = []

        for endpoint in self.get_TF_endpoints():
            poster_path_r = requests.get(endpoint)
            first_result = json.loads(poster_path_r.text).get('results')
            try:
                first_result = json.loads(poster_path_r.text).get('results')[0]
            except Exception as e:
                print(e)
                first_result = ""

            if first_result != "":
                original_title = first_result.get('original_title')
                poster_path = first_result.get('poster_path')
                poster = 'https://image.tmdb.org/t/p/w500{}'.format(poster_path)
            else:
                poster = ""

            posters.append(poster)

        return posters


if __name__ == "__main__":
    presenter = Presenter(1)
    # print(presenter.get_config())
    # print(presenter.get_TF_data())
    pprint(presenter.get_TF_posters())
