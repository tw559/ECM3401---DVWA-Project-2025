from flask import Blueprint, request, render_template, session, redirect, make_response, url_for
import sqlite3

task5_bp = Blueprint('task5', __name__)


basic_posts = [
    "Man, this forum is kinda basic...",
    "I know right, I bet they don't even have basic security features enabled",
    "LMAO"
]


shown_posts = basic_posts.copy()


def get_db_connection():
    conn = sqlite3.connect('task5_database.db')
    conn.row_factory = sqlite3.Row
    return conn


@task5_bp.route('/task5/main')
def main5():
    global shown_posts
    shown_posts = basic_posts.copy()
    return render_template('/task5/main5.html')


@task5_bp.route('/task5/forum', methods=['GET', 'POST'])
def forum5():

    session.clear()
    global shown_posts
    if request.method == 'POST':
        new_post = request.form.get('post', '')
        shown_posts.append(new_post)
        return redirect((url_for('task5.forum5')))

    resp = make_response()
    resp.set_data(render_template('/task5/forum5.html', posts=shown_posts))
    resp.set_cookie('Active Users', 'Kevin0507')

    return resp


@task5_bp.route('/task5/login', methods = ['GET', 'POST'])
def login5():

    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # SQL Query that is vulnerable to an SQL Injection Attack
        query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
        print("DEBUG: Executing query:", query)  # Debug output to see the generated query.
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(f'/task5/dashboard/{user["id"]}')
        else:
            error = "Invalid account"

    return render_template('/task5/login5.html', error = error)


@task5_bp.route('/task5/dashboard/<int:user_id>')
def dashboard5(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to find the user by their ID
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()  # Fetch one result

    # Close the connection
    conn.close()

    # If user not found, return 404
    if user is None:
        return "User not found", 404

    # Render the dashboard page with the user details
    return render_template('/task5/dashboard5.html', user=user, user_id=user_id)


@task5_bp.route('/task5/admin', methods = ['GET', 'POST'])
def admin5():

    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, password)).fetchone()
        conn.close()

        if user:
            if user['username'] == 'admin':
                session['username'] = username
                session['user_id'] = user['id']
                return redirect('/task5/admin/flagged')
            else:
                error = "Access denied: Admins only"
        else:
            error = "Invalid account"
    return render_template('/task5/admin5.html', error = error)


@task5_bp.route('/task5/admin/flagged')
def flag5():
    return render_template('/task5/flag5.html')


flag_5 = "Friendship"


@task5_bp.route('/task5/quiz', methods=['GET', 'POST'])
def quiz5():
    return render_template('/task5/quiz5.html')


@task5_bp.route('/task5/answer', methods=['POST'])
def answer5():
    correct_answer = flag_5
    user_answer = request.form.get("answer", "")

    is_correct = user_answer.lower() == correct_answer.lower()

    return render_template("/task5/answer5.html", is_correct=is_correct)
