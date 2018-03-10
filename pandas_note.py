import numpy as np
import pandas as pd

# Goal: Generate movie recommendations for a user, given the movies they have
# already watched and the ratings they gave for these movies

# Define paths
movies_path = 'ml-latest-small/movies.csv'
ratings_path = 'ml-latest-small/ratings.csv'
tags_path = 'ml-latest-small/tags.csv'
links_path = 'ml-latest-small/links.csv'

# Read from files
movies_data = pd.read_csv(movies_path, sep=',', header=None, names=['movieID',
                                                                   'title',
                                                                   'genres'])

ratings_data = pd.read_csv(ratings_path, sep=',', header=None, names=['userID',
                                                                       'movieID',
                                                                       'rating',
                                                                       'timestamp'])

tags_data = pd.read_csv(tags_path, sep=',', header=None, names=['userID',
                                                                'movieID',
                                                                'tags',
                                                                'timestamp'])

links_data = pd.read_csv(links_path, sep=',', header=None, names=['movieID',
                                                                  'imdbID',
                                                                  'tmdbID'])

# Print the first 5 rows
# print(movies_data.head())
# print(ratings_data.head())
# print(tags_data.head())
# print(links_data.head())

# Join on movieID to get ratings with movies info
rating_with_movie_info = pd.merge(ratings_data, movies_data, left_on='movieID',
                                 right_on='movieID')
print(rating_with_movie_info.head())

# pandas' Series object
userID_1 = rating_with_movie_info.userID
print(type(userID_1))
print(userID_1.head())

# pandas' DataFrame object
userID_2 = rating_with_movie_info[['userID']]
print(type(userID_2))
print(userID_2.head())

# Index
print(rating_with_movie_info.loc[0:10, ['userID']])
print(rating_with_movie_info.loc[0:10, ['movieID']])

# Match
toy_story_users = rating_with_movie_info[rating_with_movie_info.title=='Toy Story (1995)']
print(toy_story_users.head())

# Sort
sorted_data = pd.DataFrame.sort_values(rating_with_movie_info,
                                       ['userID', 'movieID'],
                                       ascending=[0, 1])
print(sorted_data.head())

# Length
total_users = max(rating_with_movie_info.userID)
total_movies = max(rating_with_movie_info.movieID)
print(total_users)
print(total_movies)

# Count
movies_per_user = rating_with_movie_info.userID.value_counts()
user_per_movie = rating_with_movie_info.title.value_counts()

print(user_per_movie.head())
