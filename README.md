# open-rec
**open-rec** is a recommendation system. The purpose is to gain a better
understanding of various **collaborative filtering methods** that are commonly
used in big system, such as Netflix, Youtube, Amazon,...

## Dataset

The dataset that I am using is from [MovieLens 100K 
Datasets](https://grouplens.org/datasets/movielens/)

> Small: 100,000 ratings and 1,300 tag applications applied to 9,000 movies by 
> 700 users. Last updated 10/2016.

## Methods

### K Nearest Neighbours

The goal is to find the k nearest neighbours of a user and use their ratings to
predict ratings of the active user for items they haven't rated yet.

### Matrix Factorization

Identify some hidden factors which influence user's ratings of an item.
We don't know these factors are. For example, in our movie dataset, 
we are not using any movies' descriptions data. We only have the movies' titles, 
movies IDs, and ratings from different users.

The way to do it is to decompose a user's item rating matrix into 2 user
matrices. One is the user-factor matrix and one is user-item matrix.
Each row in the user-factor matrix maps the user onto the hidden factor.
Each row in the user-item matrix maps the item onto the hidden factor.
These factor may or may not have any meaning in real life. They might have some
abstract meaning. We have no ideas until we have the right factorization.
This operation will be pretty expensive because it will effectively give us
the factor vectors needed to find the rating of any item by any user.
It will only perform once and then we will have all the ratings for all the
users. We then can update the matrix along the way.

## Structure

> TODO

## Testing

> TODO

## Flow

- Save the results of training sessions to disk or database (mongodb).
- Use these to build a Netflix-like interface (need to auto find movies' covers
  somehow)

## APIs

Endpoint | Description
--- | ---
`/user` | List all available users ID
`/user/<int:ID>` | Show the user's profile with given ID
`/user/<int:ID>/raw` | Show the user's raw metrics from different methods
`/dashboard` | Compare different results?
