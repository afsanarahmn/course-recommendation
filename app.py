from flask import Flask, request, session, redirect, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev'  # Change in production

def get_db():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'Welcome to Course Recommendation!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (request.form['username'],)).fetchone()
        if user and check_password_hash(user['password_hash'], request.form['password']):
            session['user_id'] = user['id']
            return redirect('/')
    return render_template('login.html')

@app.route('/api/courses')
def get_courses():
    db = get_db()
    rows = db.execute("SELECT * FROM courses").fetchall()
    return jsonify([dict(row) for row in rows])

