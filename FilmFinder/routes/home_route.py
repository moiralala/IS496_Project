# IS496: Computer Networks
# Course Mini-Project
# Name and Netid of each member:
# Member 1: chenzhao wang, cw107
# Member 2: Zhen Li, zhenli6
from flask import Flask, render_template, session, jsonify
from utils.home_utils import get_user_favorites
from app import app


@app.route('/user-home')
def user_home():
    user_id = session.get('user_id')
    if not user_id:
        # If no user is logged in, redirect to login page or return an error
        return jsonify({'error': 'User not logged in'}), 403

    return render_template('home.html')


@app.route('/user-favorites-api')
def user_favorites_api():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403

    favorite_movies, favorite_actors = get_user_favorites(user_id)
    return jsonify({
        'favorite_movies': favorite_movies,
        'favorite_actors': favorite_actors
    })
