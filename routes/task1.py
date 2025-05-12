from flask import Blueprint, request, render_template, session, redirect, render_template_string
# from app import get_db_connection
import sqlite3

task1_bp = Blueprint('task1', __name__)


def get_db_connection():
    """
    Simple function to connect to the sql database for task 1
    :return: A connection to the SQL database
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@task1_bp.route('/task1/login/', methods=['GET', 'POST'])
def login1():
    """
    Login view for task 1, contains an SQL query that is vulnerable to SQL Injections for the user to utilise in order
    to bypass knowing passwords
    :return: The login template, and if the user submits a successful POST request, redirects them to the dashboard
    """
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
            return redirect('/task1/dashboard')
        else:
            return "Invalid credentials", 401

    # Returns the login form template
    return render_template('/task1/login1.html')


@task1_bp.route('/task1/register/', methods=['GET', 'POST'])
def register1():
    """
    An extremely basic registration view that allows users to insert users into the SQL database. Vulnerable to SQL
    Injection attacks
    TODO Check whether this view can be removed
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # SQL Query that is vulnerable to an SQL Injection Attack
        query = "INSERT INTO users (username, password) VALUES ('{}', '{}')".format(username, password)
        print("DEBUG: Executing query:", query)  # Debug output to see the generated query.
        conn.execute(query)
        conn.commit()
        conn.close()

        return redirect('/task1/login/')

    # Simple registration form
    return render_template_string('''
        <h2>Register</h2>
        <form method="post">
            Username: <input type="text" name="username" /><br/>
            Password: <input type="password" name="password" /><br/>
            <input type="submit" value="Register" />
        </form>
    ''')


@task1_bp.route('/task1/dashboard')
def dashboard1():
    """
    Dashboard view that shows the users ID if they're logged in, otherwise redirects them to the login page
    :return:
    """
    # Checks that the user is logged in by checking that there's a username in the session
    if 'username' not in session:
        return "Not logged in.", 401

    username = session['username']

    # Gets the users ID from the SQL database
    conn = get_db_connection()
    query = "SELECT id FROM users WHERE username = '{}'".format(username)
    print("DEBUG: Executing query:", query)  # Debug output to see the generated query.
    user = conn.execute(query).fetchone()

    # Checks that the user's ID matches with the ID in the database, returns an error if it doesn't
    if user:
        user_id = user[0]
    else:
        return "User not found.", 404

    # If an ID is obtained, display the dashboard template with the users ID. Else, return to login
    if 'user_id' in session:
        return render_template('/task1/dashboard1.html', user_id=user_id)
    else:
        return redirect('/task1/login')


@task1_bp.route('/task1/main')
def main1():
    """
    The main page for task 1, contains buttons to take users to the task, quiz, info page and back to the index
    :return:
    """
    return render_template('/task1/main1.html')


@task1_bp.route('/task1/info')
def info1():
    """
    Contains information about SQL Injections, what they are, how they work and how to protect against them
    :return:
    """
    return render_template('/task1/info1.html')


@task1_bp.route('/task1/quiz', methods=['GET', 'POST'])
def quiz1():
    """
    Loads a quiz view that allows the user to input an answer, which is then passed to the answer view
    :return:
    """
    return render_template('/task1/quiz1.html')


flag_1 = "137727843"  # This is the 'answer' for task 1. Editing this will change the required input for /task1/answer1/


@task1_bp.route('/task1/answer', methods=['POST'])
def answer1():
    """
    Loads the answer template. If the answer is correct, tells the user they are correct and gives them a button to
    redirect to the index. If the user is incorrect, tells them that and gives them a button to go back to the quiz to
    try again
    :return:
    """
    # Gets the flag and the users answer
    correct_answer = flag_1
    user_answer = request.form.get("answer", "")

    # If they're the same, return true, else return false
    is_correct = user_answer == correct_answer

    return render_template("/task1/answer1.html", is_correct=is_correct)
