from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key_campusfix'

# Auth Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return "Access Denied: Admins Only", 403
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# Separate Student Login
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('campus.db')
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND role = 'student'", 
                              (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('register'))
        else:
            return render_template('student_login.html', error="Invalid Student credentials.")
            
    return render_template('student_login.html')

# Separate Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('campus.db')
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND role = 'admin'", 
                              (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('reports'))
        else:
            return render_template('admin_login.html', error="Invalid Admin credentials.")
            
    return render_template('admin_login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    return render_template('register.html')

@app.route('/tickets')
@login_required
@admin_required
def tickets():
    return render_template('tickets.html')

@app.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)