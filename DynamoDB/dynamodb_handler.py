from __future__ import print_function
import boto3
import json
import sys
import argparse

# Note - Do not change the class name and constructor
# You are free to add any functions to this class without changing the specifications mentioned below.
class DynamoDBHandler:

    def __init__(self, region):
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb', region_name=region)
        
    def create_and_load_data(self, tableName, fileName):
        # TODO - Create a table if not exist and load data from the file
        raise NotImplementedError
    
    def insert_movie(self, tableName, title, year, directors, actors, release_date, rating):
        # TODO - Insert a movie into the table
        raise NotImplementedError

    # TODO - define other functions
    
    def check_valid_insert_movie_args(self, args):
        if args.title is None or args.year is None or args.directors is None or args.actors is None or args.release_date is None or args.rating is None:
            return False
        # TODO - Implement other checks
        return True
    
    def dispatch(self, args):
        action = args.action
        response = ''
        if action == 'create_and_load_data':
            if args.table_name is None or args.file_name is None:
                response = 'Please provide the table name and file name'
            else:
                response = self.create_and_load_data(args.table_name, args.file_name)
        elif action == 'insert_movie':
            if not self.check_valid_insert_movie_args(args):
                response = ('Please provide the table name, title, year, directors, ' +
                    'actors, release_date, and rating\nExample usage: python ' +
                    'dynamodb_handler.py insert_movie --title "The Big New Movie" ' +
                    '--year 2015 --directors "Larry" --actors "Moe" ' +
                    '--release_date "23 Jan 2018" --rating 5.5')
            else:
                response = self.insert_movie(args.table_name, args.title, args.year, args.directors, args.actors, args.release_date, args.rating)
        elif action == 'delete_movie':
            raise NotImplementedError
        # TODO complete the dispatch function
        
        return response


def main():
    parser = argparse.ArgumentParser(description='dynamic_handler')
    operations = ['create_and_load_data',  
               'insert_movie', 
               'delete_movie', 
               'update_movie', 
               'search_movie_actor', 
               'search_movie_actor_director', 
               'print_stats',
               'delete_table', 
               ]
    
    parser.add_argument('action', help="command", choices=operations)
    
    # no need to specify the table_name, always use the default table name
    parser.add_argument("--table_name", type=str, help="name of the table", default="Movies")
    parser.add_argument("--file_name", type=str, help="name of the file")
    
    parser.add_argument("-y", "--year", type=int, help="year of the movie")
    parser.add_argument("-t", "--title", type=str, help="title of the movie")
    # directors could be single director or multiple directors separated by comma
    # this directors is used in insert_movie and update_movie
    parser.add_argument("--directors", type=str, help="director(s) of the movie")
    # actors could be single actor or multiple actors separated by comma
    # this actors is used in insert_movie and update_movie
    parser.add_argument("--actors", type=str, help="actors(s) in the movie")
    parser.add_argument("--release_date", type=str, help="release date of the movie (23 Jan 2018)")
    parser.add_argument("--rating", type=float, help="rating of the movie")
    
    # this actor is used in search_movie_actor and search_movie_actor_director
    parser.add_argument("--actor", type=str, help="actor in the movie")
    # this director is used in search_movie_actor_director
    parser.add_argument("--director", type=str, help="director of the movie")
    
    # we assume the user does not set both highest_rating_movies and lowest_rating_movies
    # optional flag for highest_rating_movies
    parser.add_argument("--highest_rating_movies", action="store_true", help="flag to get highest rating movies")
    # optional flag for lowest_rating_movies
    parser.add_argument("--lowest_rating_movies", action="store_true", help="flag to get lowest rating movies")
    
    # optional flag for setting the region (no need to specify the region, always use us-west-2 as default region)
    parser.add_argument('--region', type=str, help='The region name', default='us-west-2')
    
    args = parser.parse_args()
    handler = DynamoDBHandler(args.region)
    response = handler.dispatch(args)
    print(response)
    
    # example usage
    # python dynamodb_handler.py create_and_load_data --file_name moviedata.json
    # python dynamodb_handler.py insert_movie --year 2015 --title "The Big New Movie" --directors "Evan Goldberg, Seth Rogen" --actors "James Franco, Jonah Hill" --release_date "23 Jan 2018" --rating 5.5
    # python dynamodb_handeer.py delete_movie --title "The Big New Movie"
    # python dynamodb_handler.py update_movie --year 2015 --title "The Big New Movie" --directors "Evan Goldberg, Seth Rogen" --actors "James Franco, Jonah Hill" --release_date "23 Jan 2018" --rating 6.5
    # python dynamodb_handler.py search_movie_actor --actor "Moe"
    # python dynamodb_handler.py search_movie_actor_director --actor "Moe" --director "Evan Goldberg"
    # python dynamodb_handler.py print_stats --highest_rating_movies
    # python dynamodb_handler.py print_stats --lowest_rating_movies
    # python dynamodb_handler.py delete_table

if __name__ == '__main__':
    main()
