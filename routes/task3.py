from flask import Blueprint, request, render_template, session, redirect
import sqlite3

task3_bp = Blueprint('task3', __name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@task3_bp.route('/task3/login/', methods=['GET', 'POST'])
def login3():

    # Effectively a more secure version of the login function in task1/login1
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # Query is parameterized to avoid SQL Injections
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['user_id'] = user['id']
            return redirect('/task3/dashboard')
        else:
            return "Invalid credentials", 401

    return render_template('/task3/login3.html')


@task3_bp.route('/task3/main')
def main3():
    return render_template('task3/main3.html')


@task3_bp.route('/task3/info')
def info3():
    return render_template('task3/info3.html')


@task3_bp.route('/task3/forum')
def forum3():
    return render_template('task3/fakeblog3.html')


@task3_bp.route('/task3/dashboard')
def dashboard3():

    if 'username' not in session:
        return "Not logged in.", 401

    username = session['username']

    conn = get_db_connection()
    query = "SELECT id FROM users WHERE username = '{}'".format(username)
    print("DEBUG: Executing query:", query)  # Debug output to see the generated query.
    user = conn.execute(query).fetchone()

    if user:
        user_id = user[0]
    else:
        return "User not found.", 404

    if 'user_id' in session:
        return render_template('/task3/dashboard3.html', user_id=user_id)
    else:
        return redirect('/task3/login')


flag_3 = "675902681"


@task3_bp.route('/task3/quiz', methods=['GET', 'POST'])
def quiz3():
    return render_template('/task3/quiz3.html')


@task3_bp.route('/task3/answer', methods=['POST'])
def answer3():
    correct_answer = flag_3
    user_answer = request.form.get("answer", "")

    is_correct = user_answer == correct_answer

    return render_template("/task3/answer3.html", is_correct=is_correct)
