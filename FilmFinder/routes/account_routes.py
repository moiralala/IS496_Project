# IS496: Computer Networks
# Course Mini-Project
# Name and Netid of each member:
# Member 1: chenzhao wang, cw107
# Member 2: Zhen Li, zhenli6
from app import app
from flask import request, render_template, jsonify, session, redirect
from utils.account_utils import register_user, check_user_cred, get_user_id, is_username_available


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle user login. Extract username and password from the request.
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    # Validate credentials and set session if valid.
    if check_user_cred(user_name, password):
        user_id  = get_user_id(user_name, password)
        session['user_name'] = user_name
        session['password'] = password
        session['user_id'] = user_id
        return jsonify({'success': True, 'user_id': user_id})
    else:
        # Return error if credentials are invalid.
        return jsonify({'success': False, 'message': 'Invalid credentials'})


@app.route('/register', methods=['POST'])
def register():
    # Handle user registration. Extract username and password from the request.
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    # Check if the username is available and register the user if it is.
    if is_username_available(user_name):
        register_user(user_name, password)
        user_id = get_user_id(user_name, password)
        session['user_name'] = user_name
        session['password'] = password
        session['user_id'] = user_id
        return jsonify({'success': True, 'user_id':user_id})
    else:
        # Return error if the username is already taken.
        return jsonify({'success': False, 'message': 'Username already exists'})
    


