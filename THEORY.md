# Recommender system

*Reference: [Byte-Sized-Chunks: Recommendation
Systems](https://www.udemy.com/recommendation-systems/)*

High quality, personalized recommendation system are the holy grail for every
online stores today, wherever they are selling books, musics, or electronics.
Amazon, Spotify, Netflix are the best examples since their services are
entirely based on how good they recommend to users in in order for them to
continue using their products.

The end goal for online store is either revenue or engagement. Amazon wants
their users to spend as much time on their website to buy things that they
like. For subscription-based service like Spotify or Netflix, they want users
to spend time using their subscription services as much as possible and be
addicted to their services.

Unlike, online stores have no sales people but a huge number of products. Users
have a limited time and patient and most of the time are unsure about what they
are looking for. The recommender systems help users navigating through the maze
of online stores as well as finding what they are looking for quickly. They
also help users find things that they might like but did not know of. In
general, recommender systems solve the problem of discovery.

## Recommendation Engine

A recommendation engine takes all the user's history and the product-related
data then filter out relevant for that particular user. For each product, it
might predict what rating the user would give to a product, whether the user
would buy a product or not. It might also rank products based their relevance
to the user.

The world "relevant" could be used in many contexts. It can be what user have
bought or searched for on the website. For example, if you are interested in
Machine Learning then Machine Learning textbooks are relevant recommendations for
you. It could be something that can be used with the thing that you are looking
at right now. For example, a text on R might help even though it doesn't cover
Machine Learning topics. If you are buying a camera, camera's accessories like
lens or tripods might be useful and relevant for you.

There are different ways to find these relevant products. One way is to find
the products that are similar to the one user liked (content-based filtering).
Another way is to look for the ones that are liked by similar users
(collaborative filtering). We can also find the products that
are purchased along with the ones that user like (association rules).

**How do we know if a user like a product?**

These are the products that user purchases recently, clicks on, adds to cart or
rate highly. If the user rates something low, that also means something.
Sometimes, stores also ask for explicit input from user.

## Content-based filtering

Given a user, content-based filtering has to find products that are similar to
the products that user already like. The similarity of products is defined by
content of these products being the same. For example, if the content of two
books or two movies are similar. It could even be the description
characteristics of the two products, such as the color of two types of
shoes or the brands you trust.

Content-based filtering is normally used with text documents, such as news,
books or articles. First we start by identifying factors which describe and
differentiate products. With those metrics, we decide if the user like the
product or not. Then we will express these products in term of their
descriptors. Example of attributes for books are genre (science fiction,
comedy, drama), the words are that used in these books, the styles of writing
or the authors. We then map all the products to the factors. A user's profile
is created by using the same terms.

This key challenge in content-based filtering is to answer two questions:
- "What attributes should?"
- "How are these generated?"

Typically, we will need to manual data collection. For text documents, we could
use NLP to generate descriptors. It could be as simple as counting word
frequencies in documents. Then we could find the nearest neighbours for the
terms. For different kind of documents such as movies or songs, we need to
manually collect data every product and user is mapped against the factors that
we identify. This is also the reason that content-based filtering is less
common.

The most successful example of content-based filtering is the music genome
project owned by Pandora. It is a massive project that aims to build
descriptors for every song they have in their database. Every song is
represented by a vector of 450 "genes". Trained musical analysts score each
song on the 450 attributes. The process takes 20-30 minutes per song. The radio
then keeps playing songs that match the user's preferences.

## Collaborative filtering

What if we could recommend products without knowing anything about the products
themselves? Unlike content-based filtering, collaborative filtering doesn't
require any product description at all. Normally, if we want to find a movie to
watch, restaurant to go to, an artist to check out or a book to read, we ask a
friend who likes the same things as us. Therefore, the basic premise here is:
if 2 users have the same opinion about a bunch of products, they are likely to
have the same opinion about other products as well. For any algorithm that
relies only on user behaviors such as users’ history, ratings and so on, the
algorithm normally predicts user’ ratings for products they haven’t rated yet.
Rating can mean that a user likes a product. Explicitly, in the case of
Netflix, it asks user to rate a movie once they have watched it. Implicitly, we
can learn it from users’ clicks, purchases, searches.

There are many different algorithms to perform collaborative filtering. Two
most popular techniques are: nearest neighbour based methods and latent factor
based methods.

### Nearest neighbour based methods

The objective is to predict a user's rating for a product they haven't rated
yet. This is done by finding the neighbours of the active user. The solution is
to find the k-nearest neighbours of that user and take a weighted average of
their ratings for products. Intuitively, in order to find how a person would
like a product or not, find users that are similar to that user and take a
weighted average of their opinions.

Users who give the same ratings for a bunch of products are said to be similar
to each other. For example, two users rate same movies really high or they both
hate the same movies. If we can find the k-nearest neighbours that are most
similar to the active user then we can use their ratings for different products
to predict how this user react to a bunch of products.

We start by building a item-rating matrix, where we present users by their
ratings for different products. This matrix has n rows for all the n users in
our database and m columns for the entire list of products. It presents every
user's rating for every product that one has ever rated. Of course there are
some items which haven't been rated by a particular user or some users that
haven't rated some particular items. This happens in real life because most
users would not have rated a lot of of items and most items would not have been
rated by many users. Those particular cell will is presented as NaN.

```
        Item 1  Item 2  Item 3  Item 4  Item 5  ... Item m
User 1    4       -       4       -       -           -
User 2    -       3       4       -       -           -
User 3    5       3       2       -       5           -
User 4    2       -       2       -       -           -
User 5    4       -       4       5       -           -
     .
     .
     .
User n    4       -       4       5       -           -
```

Nearest neighbours are found using a similarity or distance metric. There are
different ways to find the similarity between 2 vectors:
- Euclidean Distance
- Cosine similarity
- Pearson correlation

**Euclidean Distance**

It is the distance measured between two points in any space. We can use the
Pythagorean theorem in any n-dimensional space to calculate the hypotenuse.

**Cosine similarity**

Find the angle between two vectors and that will be the cosine similarity. The
lower the cosine, the more similar these vectors are.

**Pearson correlation**

Given any two variables, the correlation is the measure of how similar of those
variables are or how similar the changes in those variables are. The Pearson
correlation is nothing but a correlation that you would normally measure when
you try something to do something like a linear regression. It is analogous to
cosine similarity after adjusting by the respective means. The vectors here are
users' ratings for different products. Each certain will have a certain bias.
Some will rate movies but some might have a tendency to rate everything low.

**How do we account for these biases?**
One way could be to normalize users' ratings by their average ratings. This is
exactly what the Pearson correlation does.

## Association rules
