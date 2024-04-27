from flask import jsonify
from imdb import IMDb
import logging
from .database import get_db_connection

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the IMDb API instance
ia = IMDb()

def advanced_search_movies_and_actors(criteria):
    movie_name = criteria.get('movie_name', '').strip()
    actor_name = criteria.get('actor_name', '').strip()
    genre = criteria.get('genre', '').strip()
    year = criteria.get('year', '').strip()

    # Search for movies and people
    movie_results = ia.search_movie(movie_name) if movie_name else []
    actor_results = ia.search_person(actor_name) if actor_name else []

    detailed_movies = []
    detailed_actors = []
    matched_movies = []

    # Process movie results
    for movie in movie_results:
        if len(detailed_movies) >= 10:
            break  # Limit to the first 10 movies

        try:
            movie_id = movie.movieID
            movie_details = ia.get_movie(movie_id)

            # Apply genre filter
            if genre and genre not in movie_details.get('genres', []):
                continue
            
            # Apply year filter
            if year and (not movie_details.get('year') or int(movie_details.get('year', 0)) < int(year)):
                continue

            # Process cast and match with actor name if provided
            cast_names = [person['name'] for person in movie_details.get('cast', []) if 'name' in person]
            if actor_name and actor_name in cast_names:
                # This movie is a match and should be prioritized
                matched_movies.append(movie_details)
            else:
                # This movie is not a full match but still relevant
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

    # Sort matched movies by relevance (year and rating)
    matched_movies.sort(key=lambda x: (x.get('year', 0), x.get('rating', 0)), reverse=True)

    # Add matched movies to the front of the detailed movies list
    for matched_movie in matched_movies[:10]:  # Ensure we don't exceed 10 total
        detailed_movies.insert(0, {
            'title': matched_movie.get('title'),
            'year': matched_movie.get('year'),
            'genres': matched_movie.get('genres'),
            'rating': matched_movie.get('rating'),
            'cast': [person['name'] for person in matched_movie.get('cast', [])[:3] if 'name' in person],
            'plot': matched_movie.get('plot outline'),
            'movie_id': matched_movie.movieID
        })

    # Process actor results
    for actor in actor_results:
        if len(detailed_actors) >= 10:
            break  # Limit to the first 10 actors

        try:
            actor_id = actor.personID
            actor_details = ia.get_person(actor_id)
            detailed_actors.append({
                'name': actor_details.get('name'),
                'actor_id': actor_id,
                'biography': actor_details.get('mini biography', []),
                'filmography': [film['title'] for film in actor_details.get('filmography', {}).get('actor', [])][:3]
            })
        except Exception as e:
            logging.error("Error fetching actor details for ID %s: %s", actor.personID, e)

    # Limit the detailed movies list to the top 10 if necessary
    detailed_movies = detailed_movies[:10]

    # Combine detailed movies with actor results
    combined_results = {
        'Movies': detailed_movies,
        'Actors': detailed_actors
    }

    return combined_results