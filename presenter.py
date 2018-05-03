"""
    presenter.py - Presenter parses data and gets TMDb poster links
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
        Initialize a Presenter object to read and process data.

        Params:
            None

        Return:
            None
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
        Parse string to URL scheme.

        Params:
            data <str>: Data to process

        Return:
            List of workable string endpoints.
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
        Get configurations.

        Params:
            None

        Return:
            Configuration data in dictionary format.
        """
        return self.config

    def get_data(self, method):
        """
        Get trained data for a specific method.

        Params:
            method <str>: Method to get

        Return:
            Data in dictionary format.
        """
        if method == 'TF':
            data = self.TF_data
        elif method == 'NN':
            data = self.NN_data
        elif method == 'LF':
            data = self.LF_data

        return data

    def get_endpoints(self, method):
        """
        Get processed endpoints for a specific method.

        Params:
            method <str>: Method to get

        Return:
            List of workable string endpoints.
        """
        endpoints = []

        if method == 'TF':
            data = self.TF_data
        elif method == 'NN':
            data = self.NN_data
        elif method == 'LF':
            data = self.LF_data

        for item in self.process(data):
            endpoints.append(item)

        return endpoints

    def get_posters(self, method, n):
        """
        Get posters with titles and links for a specific method.

        Params:
            method <str>: Method to get
            n <int>: Number of returned posters

        Return:
            List of poster objects with titles and links.
        """
        poster_paths = []
        for endpoint in self.get_endpoints(method):
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

            poster_paths.append(poster)
        
        titles = self.get_data(method)
        posters = []
        for i in range(len(titles)):
            posters.append({
                'title': titles[i],
                'link': poster_paths[i]
            })

        return posters[:n]
