"""
    config.py - Configuration hub
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/21/18
"""

LOGO = """

    █▀▀█ █▀▀█ █▀▀ █▀▀▄ ░ ░ █▀▀▄ █▀▀ █▀▀
    █░░█ █░░█ █▀▀ █░░█ ▀ ▀ █░░█ █▀▀ █░░
    ▀▀▀▀ █▀▀▀ ▀▀▀ ▀░░▀ ░ ░ ▀▀▀░ ▀▀▀ ▀▀▀

"""

# TMDB API
TMDB_API_KEY = '5aa9602e93b97cbbc78fb33204297c2a'
MOVIE_SEARCH_ENDPOINT = 'https://api.themoviedb.org/3/search/movie?api_key={}&query='.format(TMDB_API_KEY)

# Dataset location
RATINGS_PATH = 'ml-latest-small/ratings.csv'
MOVIES_PATH = 'ml-latest-small/movies.csv'

# Matrix factorization constants
MF_DEBUG = True
MF_STEPS = 100
MF_GAMMA = 0.001
MF_LAMDA = 0.02

# Number of recommendation output 
NUMS_RECOMMENDATIONS = 10

# For target_random and build data only
NUMS_WORKERS = 1
MIN_ID = 1
MAX_ID = 101

# For target_one only 
TARGET_ID = 1
