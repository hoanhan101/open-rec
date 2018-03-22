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

# Dataset location
RATINGS_PATH = 'ml-latest-small/ratings.csv'
MOVIES_PATH = 'ml-latest-small/movies.csv'

# Matrix factorization constants
MF_STEPS = 3
MF_GAMMA = 0.001
MF_LAMDA = 0.02

# Worker
NUMS_WORKERS = 1
NUMS_RECOMMENDATIONS = 3
MAX_ID = 10
