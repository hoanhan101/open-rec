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
MF_DEBUG = False
MF_STEPS = 5
MF_GAMMA = 0.001
MF_LAMDA = 0.02

# Workers settings
NUMS_WORKERS = 1
NUMS_RECOMMENDATIONS = 5
MAX_ID = 10

# Target only 1 user
TARGET_ID = 1
