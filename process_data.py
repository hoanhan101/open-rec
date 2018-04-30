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


if __name__ == "__main__":
    root = 'https://api.themoviedb.org/3/search/movie?api_key={}&language={}&query='.format(TMDB_API_KEY,
                                                                                            'en-US')

    for i in range(1, 2):
        persister = Persister(i)
        data = persister.read()
        LF_data = data.get('data').get('latent_factors')
        for movie in LF_data:
            query = urllib.parse.quote(movie)
            endpoint = root + query + '&page=1&include_adult=false'
            poster_path_r = requests.get(endpoint)
            first_result = json.loads(poster_path_r.text).get('results')[0]
            original_title = first_result.get('original_title')
            poster_path = first_result.get('poster_path')
            image_r = requests.get('https://image.tmdb.org/t/p/w500/{}'.format(poster_path))
            pprint(image_r)
            break
