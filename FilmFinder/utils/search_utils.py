# IS496: Computer Networks
# Course Mini-Project
# Name and Netid of each member:
# Member 1: chenzhao wang, cw107
# Member 2: Zhen Li, zhenli6
from flask import jsonify
from imdb import IMDb
import logging
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from .database import get_db_connection

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the IMDb API instance
ia = IMDb()

# Implement caching to avoid repeated API calls
@lru_cache(maxsize=512)
def get_movie_details(movie_id):
    # Retrieve detailed movie information based on the movie ID.
    return ia.get_movie(movie_id)


@lru_cache(maxsize=512)
def get_actor_details(actor_id):
    # Retrieve detailed actor information based on the actor ID.
    return ia.get_person(actor_id)


# Process movie search criteria
def process_movies(criteria):
    # Extract search criteria and perform movie search on IMDb.
    movie_name = criteria.get('movie_name', '').strip()
    genre = criteria.get('genre', '').strip()
    year = criteria.get('year', '').strip()
    actor_name = criteria.get('actor_name', '').strip()
    movie_results = ia.search_movie(movie_name) if movie_name else []
    detailed_movies = []
    matched_movies = []

    # Process search results and filter according to additional criteria.
    for movie in movie_results:
        if len(detailed_movies) >= 10:
            break
        try:
            movie_id = movie.movieID
            movie_details = get_movie_details(movie_id)
            if genre and genre not in movie_details.get('genres', []):
                continue
            if year and (not movie_details.get('year') or int(movie_details.get('year', 0)) < int(year)):
                continue
            cast_names = [person['name'] for person in movie_details.get('cast', []) if 'name' in person]
            if actor_name and actor_name in cast_names:
                matched_movies.append(movie_details)
            else:
                detailed_movies.append({
                    'title': movie_details.get('title'),
                    'year': movie_details.get('year'),
                    'genres': movie_details.get('genres'),
                    'rating': movie_details.get('rating'),
                    'cast': cast_names[:3],
                    'plot': movie_details.get('plot outline'),
                    'movie_id': movie_id
                })
        except Exception as e:
            logging.error("Error fetching movie details for ID %s: %s", movie.movieID, e)
    matched_movies.sort(key=lambda x: (x.get('year', 0), x.get('rating', 0)), reverse=True)
    for matched_movie in matched_movies[:10]:
        detailed_movies.insert(0, {
            'title': matched_movie.get('title'),
            'year': matched_movie.get('year'),
            'genres': matched_movie.get('genres'),
            'rating': matched_movie.get('rating'),
            'cast': [person['name'] for person in matched_movie.get('cast', [])[:3] if 'name' in person],
            'plot': matched_movie.get('plot outline'),
            'movie_id': matched_movie.movieID
        })
    return detailed_movies[:10]


# Process actor search criteria
def process_actors(criteria):
    actor_name = criteria.get('actor_name', '').strip()
    actor_results = ia.search_person(actor_name) if actor_name else []
    detailed_actors = []

    for actor in actor_results:
        if len(detailed_actors) >= 10:
            break
        try:
            actor_id = actor.personID
            actor_details = get_actor_details(actor_id)
            detailed_actors.append({
                'name': actor_details.get('name'),
                'actor_id': actor_id,
                'biography': actor_details.get('mini biography', []),
                'filmography': [film['title'] for film in actor_details.get('filmography', {}).get('actor', [])][:3]
            })
        except Exception as e:
            logging.error("Error fetching actor details for ID %s: %s", actor.personID, e)
    return detailed_actors


def advanced_search_movies_and_actors(criteria):
    # Use ThreadPoolExecutor to process movies and actors searches concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        movie_future = executor.submit(process_movies, criteria)
        actor_future = executor.submit(process_actors, criteria)

    detailed_movies = movie_future.result()
    detailed_actors = actor_future.result()

    return {
        'Movies': detailed_movies,
        'Actors': detailed_actors
    }
