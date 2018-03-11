import numpy as np
import pandas as pd

from scipy.spatial.distance import correlation

# Here are the paths to our data
ratings_path = 'ml-latest-small/ratings.csv'
movies_path = 'ml-latest-small/movies.csv'

# Read CSV files
ratings_data = pd.read_csv(ratings_path)
movies_data = pd.read_csv(movies_path, usecols=[0, 1])

# Rename columns
ratings_data.columns = ['userID', 'movieID', 'rating', 'timestamp']
movies_data.columns = ['movieID', 'title']

# Make sure the data types are correct
if ratings_data.userID.dtypes != 'int64':
    raise TypeError

if ratings_data.movieID.dtypes != 'int64' and movies_data.movieID.dtypes != 'int64':
    raise TypeError

if ratings_data.rating.dtypes != 'float64':
    raise TypeError

if ratings_data.timestamp.dtypes != 'int64':
    raise TypeError

# ----------------
# HELPER FUNCTIONS
# ----------------

def find_top_favorite_movies(active_user, n):
    """
    Find the top n movies for a given user.
    Params:
        active_user (int): User ID
        n (n): Number of top movies

    Return:
        List of movies' titles

    Steps:
        Get a list of user that matched the ID
        Sort the list by rating in ascending order
        Return only the titles of the movies
    """
    top_movies = pd.DataFrame.sort_values(
        ratings_data[ratings_data.userID==active_user],
        ['rating'],
        ascending=[0]
    )[:n]
    return list(top_movies.title)

# -----------------------
# FINDING RECOMMENDATIONS
# -----------------------

# Start by using a neighbour based collaborative filtering model.
# Need to find the k nearest neighbours of a user and use their ratings to
# predict ratings of the active user for movies they haven't rated yet.

# Need to present each user as a vector.
# Each element of the vector will be their rating for 1 movie.
# When user doesn't have any rating for a movie, the corresponding component
# will be NaN, aka Not a Number.

# pivot_table in pandas is similar to Pivot table in Excel or GroupBy in SQL.
# Let userID be index row and movieID be column, value is the result of
# aggregated function to calculate the mean rating rating for that movie.
user_item_rating_matrix = pd.pivot_table(ratings_data,
                                         values='rating',
                                         index=['userID'],
                                         columns=['movieID']
                                        )

# Join on movieID to get ratings with movies info
ratings_data = pd.merge(ratings_data, movies_data, left_on='movieID',
                                 right_on='movieID')

# There are a lot of NaN here because it is expected that movies would not have
# been rated by multiple users or many users would not have rated a lot of
# movies.
# print(user_item_rating_matrix.head())

# Now each user has been represented using their ratings.
# Need to find the similarity between 2 users.
# Use a correlation.
def find_similarity(user_1, user_2):
    """
    Compute the similarity between 2 users.

    Params:
        user_1 (array): User 1's vector
        user_2 (array): User 2's vector

    Return:
        The correlation of these 2 vectors.
    """
    # Normalize for any biases that users might have.
    # For example:
    #   - some users might be bias by high ratings, they are just generous.
    #   - some are more ciritical so they give lower rating in general
    # Make sure that any bias which is specific to that user
    # is removed.
    # np.nanmean() returns the mean of an array after ignoring 
    user_1 = np.array(user_1) - np.nanmean(user_1)
    user_2 = np.array(user_2) - np.nanmean(user_2)

    # Subset each user to be represented only by the ratings for the movies
    # that both of them have rated.
    # This gives us movies for which both users have non NaN ratings.
    common_movieIDs = [i for i in range(len(user_1)) if user_1[i] > 0 and
                       user_2[i] > 0]

    if common_movieIDs == 0:
        # There are no movies in common
        return 0
    else:
        # Subset each of the user to have only the ratings for common movies,
        # then find the correlation between these 2 vectors.
        user_1 = np.array([user_1[i] for i in common_movieIDs])
        user_2 = np.array([user_2[i] for i in common_movieIDs])
        return correlation(user_1, user_2)

# We have a function to compute the similarity between 2 users, we can use this
# to computer the similarity between the active user and every other users and
# find the nearest neighbours of the active user.
def find_nearest_neighbour_ratings(active_user, k):
    """
    Find k nearest neighbour of the active user then use their ratings to
    predict the active users rating for other movies.

    Params:
        active_user (array): User's vector
        k (int): Number of nearest neighbour we have to find

    Return:
        DataFrame of predicted ratings.
    """
    # Create an empty matrix who row index is user ID and the value will be the
    # similarity of that user to the active user
    similarity_matrix = pd.DataFrame(index=user_item_rating_matrix.index,
                                    columns=['Similarity'])

    for i in user_item_rating_matrix.index:
        similarity_matrix.loc[i] = find_similarity(
                                        user_item_rating_matrix.loc[active_user],
                                        user_item_rating_matrix.loc[i])

    # Sort the similarity matrix in the descending other of similarity
    similarity_matrix = pd.DataFrame.sort_values(similarity_matrix,
                                                ['Similarity'],
                                                ascending=[0])

    # Get only the top k numbers of nearest neighbours
    nearest_neighbours = similarity_matrix[:k]

    # Use their ratings to predict active users' rating for every movie
    neightbour_items_ratings = user_item_rating_matrix.loc[nearest_neighbours.index]

    # This is a placeholder for the predicted items ratings.
    # Its row index is the list of movies IDs
    predicted_ratings = pd.DataFrame(index=user_item_rating_matrix.columns,
                                        columns=['Rating'])

    for i in user_item_rating_matrix.columns:
        # Start with the average rating of the user
        predicted_rating = np.nanmean(user_item_rating_matrix.loc[active_user])

        # For each neighbour in the nearest neighbours list
        for j in neightbour_items_ratings.index:
            # If the neighbour has rated that movie, 
            # add the rating of the neighbour for that movie, 
            # adjusted by the average rating of that neighbour,
            # weighted by the similarity of the neighbour to the active user
            if user_item_rating_matrix.loc[j, i] > 0:
                predicted_rating += (
                    user_item_rating_matrix.loc[j, i]
                    - np.nanmean(user_item_rating_matrix.loc[j])
                ) * nearest_neighbours.loc[j, 'Similarity']

        # Add the rating to the predicted rating matrix
        predicted_ratings.loc[i, 'Rating'] = predicted_rating

    return predicted_ratings

def find_top_n_recommendations(active_user, n):
    """
    Find n top recommendations for the active user.

    Params:
        active_user (int): User's ID
        n (int): Number of recommendations

    Return:
        List of recommendations titles (string)
    """
    # Use the 10 nearest neighbours to find the predicted ratings
    predicted_ratings = find_nearest_neighbour_ratings(active_user, 10)

    # Drop all the movies that user has already watched
    # First, subset the user item rating matrix,
    # through the active user's rating
    # From that row, check which movies have rating > 0,
    # put them into a list,  drop the corresponding row
    watched_movies = list(
        user_item_rating_matrix.loc[
            active_user
        ].loc[user_item_rating_matrix.loc[active_user]>0].index
    )

    predicted_ratings = predicted_ratings.drop(watched_movies)

    # This gives us the list of movies IDs which are top recommendations
    top_recommendations = pd.DataFrame.sort_values(predicted_ratings,
                                                   ['Rating'],
                                                   ascending=[0])[:n]

    top_recommendations_titles = (
        movies_data.loc[
            movies_data.movieID.isin(top_recommendations.index)
        ]
    )

    return list(top_recommendations_titles.title)


if __name__ == "__main__":
    active_user = 5
    limit = 5
    print(find_top_n_recommendations(active_user, limit))
    print(find_top_favorite_movies(active_user, limit))
