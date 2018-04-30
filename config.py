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
MF_DEBUG = True
MF_STEPS = 1000
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
