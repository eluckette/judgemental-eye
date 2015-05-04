"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    with open('./seed_data/u.user') as source_file:
        for line in source_file:
            user_data = line.rstrip().split('|')
            user = User(user_id=user_data[0], age=user_data[1], zipcode=user_data[4])
            db.session.add(user)
        db.session.commit()

def load_movies():
    """Load movies from u.item into database."""
    
    with open('./seed_data/u.item') as source_file:
        for line in source_file:
            movie_data = line.rstrip().split('|')
            
            if movie_data[2] != '':
                movie_release_date = datetime.strptime(movie_data[2], '%d-%b-%Y')
            
            else:        
                movie_release_date = datetime(0001,01,01)

            movie = Movie(movie_id=movie_data[0], 
                          title=movie_data[1][:-7], 
                          released_at=movie_release_date, 
                          imdb_url=movie_data[4])
            
            db.session.add(movie)
        db.session.commit()



def load_ratings():
    """Load ratings from u.data into database."""

    with open('./seed_data/u.data') as source_file:
        for line in source_file:
            rating_data = line.rstrip().split('\t')
            rating = Rating(movie_id=rating_data[1], 
                          user_id=rating_data[0], 
                          score=rating_data[2])
            
            db.session.add(rating)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
