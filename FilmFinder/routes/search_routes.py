from flask import Flask, request, jsonify, render_template
from utils.search_utils import advanced_search_movies_and_actors
from app import app 

@app.route('/search-page')
def search_page():
    # Render search.html
    return render_template('search.html')

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
