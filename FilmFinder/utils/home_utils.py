from .database import get_db_connection
from imdb import IMDb

ia = IMDb()
def get_user_favorites(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get favorite movie IDs
    cur.execute('SELECT movie_id FROM Favorites WHERE user_id = ? AND movie_id IS NOT NULL', (user_id,))
    movie_ids = [row['movie_id'] for row in cur.fetchall()]

    # Get favorite actor IDs
    cur.execute('SELECT actor_id FROM Favorites WHERE user_id = ? AND actor_id IS NOT NULL', (user_id,))
    actor_ids = [row['actor_id'] for row in cur.fetchall()]

    # Fetch summarized movie details from IMDb
    list_movies = []
    for movie_id in movie_ids:
        movie_details = ia.get_movie(movie_id)
        list_movies.append({
            'title': movie_details.get('title'),
            'year': movie_details.get('year'),
            'genres': movie_details.get('genres', []),
            'rating': movie_details.get('rating'),
            'movie_id': movie_id
        })

    # Fetch summarized actor details from IMDb
    list_actors = []
    for actor_id in actor_ids:
        actor_details = ia.get_person(actor_id)
        list_actors.append({
            'name': actor_details.get('name'),
            'known_for': [film['title'] for film in actor_details.get('filmography', {}).get('actor', [])[:3]],
            'actor_id': actor_id
        })

    conn.close()
    return list_movies, list_actors

