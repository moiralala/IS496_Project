from app import app
from flask import request, render_template, jsonify, session
from utils.account_utils import register_user, check_user_cred, get_user_id, is_username_available

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    if check_user_cred(user_name, password):
        user_id  = get_user_id(user_name, password)
        session['user_name'] = user_name
        session['password'] = password
        session['user_id'] = user_id
        return jsonify({'success': True, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/register', methods=['POST'])
def register():
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    if is_username_available(user_name):
        register_user(user_name, password)
        user_id = get_user_id(user_name, password)
        session['user_name'] = user_name
        session['password'] = password
        session['user_id'] = user_id
        return jsonify({'success': True, 'user_id':user_id})
    else:
        return jsonify({'success': False, 'message': 'Username already exists'})
    


