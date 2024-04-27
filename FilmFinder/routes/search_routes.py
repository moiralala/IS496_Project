from flask import Flask, request, jsonify, render_template, session
from utils.search_utils import advanced_search_movies_and_actors
from utils.database import get_db_connection
from app import app 

@app.route('/search-page')
def search_page():
    # Render search.html
    user_id = session.get('user_id', None)
    return render_template('search.html', user_id=user_id)

@app.route('/search-api', methods=['GET'])
def search_api():
    criteria = {
        'movie_name': request.args.get('movie_name', '').strip(),
        'actor_name': request.args.get('actor_name', '').strip(),
        'genre': request.args.get('genre', '').strip(),
        'year': request.args.get('year', '').strip()
    }
    
    if criteria['year'] and not criteria['year'].isdigit():
        return jsonify({'error': 'Invalid year format'}), 400

    try:
        results = advanced_search_movies_and_actors(criteria)
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Failed to process search: {str(e)}")
        return jsonify({'error': 'Server Error'}), 500


#collect moives or actors into favorite list
@app.route('/add-favorite', methods=['POST'])
def add_favorite():
    data = request.get_json()
    user_id = session['user_id']
    movie_id = data.get('movie_id')
    actor_id = data.get('actor_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the favorite already exists to prevent duplicates
    cur.execute('SELECT 1 FROM Favorites WHERE user_id = ? AND (movie_id = ? OR actor_id = ?)',
                (user_id, movie_id, actor_id))
    exists = cur.fetchone()

    if not exists:
        cur.execute('INSERT INTO Favorites (user_id, movie_id, actor_id) VALUES (?, ?, ?)',
                    (user_id, movie_id, actor_id))
        conn.commit()
        message = 'Favorite added successfully!'
    else:
        message = 'Favorite already exists.'

    conn.close()
    return jsonify({'success': not exists, 'message': message})