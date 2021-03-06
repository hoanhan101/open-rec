"""
    open_rec.py - Recommender Logic
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 03/17/18
    Reference: Udemy's Byte-Sized-Chunks: Recommendation Systems
    (https://www.udemy.com/recommendation-systems/)
"""

import warnings
import datetime
import pickle

import itertools
import numpy as np
import pandas as pd
from scipy.spatial.distance import correlation

from config import *


class OpenREC():
    def __init__(self, ratings_path=RATINGS_PATH, movies_path=MOVIES_PATH):
        """
        Initizalize a Recommender object.

        Params:
            ratings_path: Dataset's rating path
            movies_path: Dataset's movie path

        Return:
            None
        """
        # Read CSV files
        self.ratings_data = pd.read_csv(ratings_path)
        self.movies_data = pd.read_csv(movies_path, usecols=[0, 1])

        # Rename columns
        self.ratings_data.columns = ['userID', 'movieID', 'rating', 'timestamp']
        self.movies_data.columns = ['movieID', 'title']

        # Make sure the data types are correct
        if self.ratings_data.userID.dtypes != 'int64':
            raise TypeError

        if self.ratings_data.movieID.dtypes != 'int64' and movies_data.movieID.dtypes != 'int64':
            raise TypeError

        if self.ratings_data.rating.dtypes != 'float64':
            raise TypeError

        if self.ratings_data.timestamp.dtypes != 'int64':
            raise TypeError

        # Persistent state
        self.collisions = []
        self.nearest_neighbours_store = {}

        # pivot_table in pandas is similar to Pivot table in Excel or GroupBy in SQL.
        # Let userID be index row and movieID be column, value is the result of
        # aggregated function to calculate the mean rating rating for that movie.
        self.user_item_rating_matrix = pd.pivot_table(self.ratings_data,
                                                 values='rating',
                                                 index=['userID'],
                                                 columns=['movieID']
                                                )

        # Join on movieID to get ratings with movies info
        self.ratings_data = pd.merge(self.ratings_data, self.movies_data,
                                     left_on='movieID', right_on='movieID')

    def find_top_favorite_movies(self, active_user, n):
        """
        Find the top n movies for a given user.

        Details:
            Get a list of user that matched the ID
            Sort the list by rating in ascending order
            Return only the titles of the movies

        Params:
            active_user (int): User ID
            n (int): Number of top movies

        Return:
            List of movies' titles
        """
        top_movies = pd.DataFrame.sort_values(
            self.ratings_data[self.ratings_data.userID==active_user],
            ['rating'],
            ascending=[0]
        )[:n]
        return list(top_movies.title)

    def find_similarity(self, user_1, user_2):
        """
        Compute the similarity between 2 users.

        Details:
            Now each user has been represented using their ratings.
            Need to find the similarity between 2 users.
            Use a correlation.

        Params:
            user_1 (array): User 1's vector
            user_2 (array): User 2's vector

        Return:
            The correlation of these 2 vectors.
        """
        # Normalize for any biases that users might have.
        # For example, some users might be bias by high ratings, they are just generous.
        # Some are more ciritical so they give lower rating in general.
        # Make sure that any bias which is specific to that user is removed.
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

    def find_nearest_neighbour_ratings(self, active_user, k):
        """
        Find k nearest neighbour of the active user then use their ratings to
        predict the active users rating for other movies.

        Details:
            We have a function to compute the similarity between 2 users, we can use this
            to computer the similarity between the active user and every other users and
            find the nearest neighbours of the active user.

        Params:
            active_user (array): User's vector
            k (int): Number of nearest neighbour we have to find

        Return:
            DataFrame of predicted ratings.
        """
        # Create an empty matrix who row index is user ID and the value will be the
        # similarity of that user to the active user
        similarity_matrix = pd.DataFrame(index=self.user_item_rating_matrix.index,
                                        columns=['Similarity'])

        for i in self.user_item_rating_matrix.index:
            similarity_matrix.loc[i] = self.find_similarity(
                                            self.user_item_rating_matrix.loc[active_user],
                                            self.user_item_rating_matrix.loc[i])

        # Sort the similarity matrix in the descending other of similarity
        similarity_matrix = pd.DataFrame.sort_values(similarity_matrix,
                                                    ['Similarity'],
                                                    ascending=[0])

        # Get only the top k numbers of nearest neighbours
        nearest_neighbours = similarity_matrix[:k]

        # Use their ratings to predict active users' rating for every movie
        neighbour_items_ratings = self.user_item_rating_matrix.loc[nearest_neighbours.index]

        # This is a placeholder for the predicted items ratings.
        # Its row index is the list of movies IDs
        predicted_ratings = pd.DataFrame(index=self.user_item_rating_matrix.columns,
                                            columns=['Rating'])

        for i in self.user_item_rating_matrix.columns:
            # Start with the average rating of the user
            predicted_rating = np.nanmean(self.user_item_rating_matrix.loc[active_user])

            # For each neighbour in the nearest neighbours list
            for j in neighbour_items_ratings.index:
                # If the neighbour has rated that movie, 
                # add the rating of the neighbour for that movie, 
                # adjusted by the average rating of that neighbour,
                # weighted by the similarity of the neighbour to the active user
                if self.user_item_rating_matrix.loc[j, i] > 0:
                    predicted_rating += (
                        self.user_item_rating_matrix.loc[j, i]
                        - np.nanmean(self.user_item_rating_matrix.loc[j])
                    ) * nearest_neighbours.loc[j, 'Similarity']

            # Add the rating to the predicted rating matrix
            predicted_ratings.loc[i, 'Rating'] = predicted_rating

        return predicted_ratings

    def find_top_n_recommendations(self, active_user, n):
        """
        Find n top recommendations for the active user.

        Params:
            active_user (int): User's ID
            n (int): Number of recommendations

        Return:
            List of recommendations titles (string)
        """
        # Use the 10 nearest neighbours to find the predicted ratings
        predicted_ratings = self.find_nearest_neighbour_ratings(active_user, 10)

        # Drop all the movies that user has already watched
        # First, subset the user item rating matrix,
        # through the active user's rating
        # From that row, check which movies have rating > 0,
        # put them into a list,  drop the corresponding row
        watched_movies = list(
            self.user_item_rating_matrix.loc[
                active_user
            ].loc[self.user_item_rating_matrix.loc[active_user]>0].index
        )

        predicted_ratings = predicted_ratings.drop(watched_movies)

        # This gives us the list of movies IDs which are top recommendations
        top_recommendations = pd.DataFrame.sort_values(predicted_ratings,
                                                       ['Rating'],
                                                       ascending=[0])[:n]

        top_recommendations_titles = (
            self.movies_data.loc[
                self.movies_data.movieID.isin(top_recommendations.index)
            ]
        )

        return list(top_recommendations_titles.title)

    def perform_matrix_factorization(self, R, K, steps=MF_STEPS,
                                     gamma=MF_GAMMA, lamda=MF_LAMDA):
        """
        Perform matrix factorization algorithm.

        Details:
            In user item rating matrix R, each row represent an user, each column 
            represent a user's rating for an item.
            We use Stochastic gradient descent (SGD) to find the factor vectors.
            Steps, gamma, lamda are parameters that SGD will use.

        Params:
            R (array): User-item rating matrix 
            K (int): Number of factors we will find
            steps (int): Number of steps
            gamma (float): Size of the step
            lamda (float): Value of regularization

        Return:
            P and Q matrix (array)
        """
        # N is the number of users, M is the number of items.
        N = len(R.index)
        M = len(R.columns)

        # We decompose R into P and Q matrix, where P is the user-facotr matrix, Q
        # is the user-item matrix.

        # P has N rows for users and K columns for items.
        # We initialize this matrix with some random numbers, then we iteratively
        # adjust the value of P so it moves to a place where the dot product of P
        # and Q will be very close the the user-item matrix.
        P = pd.DataFrame(np.random.rand(N, K), index=R.index)

        # Q has M rows for items.
        Q = pd.DataFrame(np.random.rand(M, K), index=R.columns)

        # SGD loops through the ratings in the user-item rating matrix.
        # It will do this as many times as we specify or until the error we are
        # minimizing reaches a certain threshold.
        for step in range(steps):
            for i in R.index:
                for j in R.columns:
                    # For each rating that exists in the training set
                    if R.loc[i,j] > 0:
                        # This is the error for one rating.
                        # It is the difference between the actual value of the
                        # rating and the predicted value (dot product of the
                        # corresponding user-factor vector and item-factor vector)
                        eij = R.loc[i, j] - np.dot(P.loc[i], Q.loc[j])

                        # We have an error function to minimize.
                        # The Ps and Qs should be moved in the downward direction
                        # of the slope of the vector at the current point.
                        # The value in the brackets is the partial derivative of
                        # the error function, i.e the slope.
                        # Lamda is the value of the regularization parameter which
                        # penalizes the model for the number of factors we are
                        # finding.
                        P.loc[i] = P.loc[i] + gamma*(eij*Q.loc[j] - lamda*P.loc[i])
                        Q.loc[j] = Q.loc[j] + gamma*(eij*P.loc[i] - lamda*Q.loc[j])

            # We have looped through all the rating once.
            # Check the value of the error function to see if we have
            # reached the threshold at which we want to stop, else we will
            # repeat the process.
            e = 0
            for i in R.index:
                for j in R.columns:
                    if R.loc[i, j] > 0:
                        e = e + pow(
                            R.loc[i,j] - np.dot(P.loc[i], Q.loc[j]), 2
                            ) + lamda*(
                                pow(
                                    np.linalg.norm(P.loc[i]), 2
                                ) + pow(
                                    np.linalg.norm(Q.loc[j]), 2
                                )
                            )

            if e < 0.001:
                break

            if MF_DEBUG == True:
                print('{} - Step {}/{}'.format(datetime.datetime.now(), step + 1, steps))

        return P, Q

    def get_top_favorites(self, uid, active_user, limit):
        """
        Get top n movies for a given user.

        Params:
            uid (int): UID
            active_user (int): UserID
            limit (int): Numbers of movies

        Return:
            List of items
        """
        self.debug(method='Top Favorites', uid=uid, active_user=active_user)

        results = []

        movies = self.find_top_favorite_movies(active_user, limit)

        for movie in movies:
            results.append(movie)
            print('- {}'.format(movie))

        return results

    def execute_nearest_neighbour(self, uid, active_user, limit):
        """
        Execute the nearest neighbour technique.

        Params:
            uid (int): UID
            active_user (int): UserID
            limit (int): Number of recommendations

        Return:
            List of items
        """
        self.debug(method='Nearest Neighbours', uid=uid, active_user=active_user)

        results = []

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recommendations = self.find_top_n_recommendations(active_user, limit)

        for item in recommendations:
            self.nearest_neighbours_store[item] = 1
            results.append(item)
            print('- {}'.format(item))

        return results

    def execute_latent_factor(self, uid, active_user, limit):
        """
        Execute latent factor technique.
        Ideally we should run this over the entire matrix for a few 1000 steps.
        This will be pretty expensive. For now, we just run it over a part of the
        matrix to see how it works.

        Params:
            uid (int): UID
            active_user (int): UserID
            limit (int): Number of recommendations

        Return:
            List of items
        """
        self.debug(method='Latent Factors', uid=uid, active_user=active_user)

        results = []

        try:
            P = pd.read_pickle('output/pkl/P.pkl')
            Q = pd.read_pickle('output/pkl/Q.pkl')
        except FileNotFoundError as e:
            print(e)

            (P, Q) = self.perform_matrix_factorization(
                self.user_item_rating_matrix, 2
            )

            P.to_pickle('output/pkl/P.pkl')
            Q.to_pickle('output/pkl/Q.pkl')

        predicted_ratings = pd.DataFrame(
            np.dot(P.loc[active_user], Q.T), index=Q.index, columns=['Rating']
        )

        # We found the ratings of all movies by the active user and 
        # then sorted them to find the top n movies 
        top_recommendations = pd.DataFrame.sort_values(
            predicted_ratings, ['Rating'], ascending=[0]
        )[:limit]

        top_recommendations_titles = self.movies_data.loc[
            self.movies_data.movieID.isin(top_recommendations.index)
        ]

        for item in list(top_recommendations_titles.title):
            if item in self.nearest_neighbours_store:
                self.collisions.append(item)

            results.append(item)
            print('- {}'.format(item))

        return results

    def check_collisions(self, uid, active_user):
        """
        Check items collisions.

        Params:
            uid (int): UID
            active_user (int): UserID

        Return:
            List of items
        """
        self.debug(method='Check Collisions', uid=uid, active_user=active_user)

        results = []

        if len(self.collisions) == 0:
            results.append('No overlapping items')
            print('- There is no collisions')
        else:
            print('Here are the same items that occured in both techniques:')
            for item in self.collisions:
                results.append(item)
                print('- {}'.format(item))

        return results

    def debug(self, method, uid, active_user):
        """
        Print custom debugging message.

        Params:
            method (string): Method
            uid (int): UID
            active_user (int): UserID

        Return:
            None
        """
        print('\n{} - Worker: {}, UserID: {}, Method: {}'.format(datetime.datetime.now(), 
                                                                 uid,
                                                                 active_user,
                                                                 method))
