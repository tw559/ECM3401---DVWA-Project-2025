from flask import Blueprint, request, render_template, session, redirect, render_template_string, make_response, url_for

task2_bp = Blueprint('task2', __name__)

# For this task (XSS Attack), the task uses a dictionary instead of the SQL database.
users = {
    'admin': 'password123',  # Here as a testing account for the login functionality
    'Adam5234': '7Ab64EBzxmgCt7yG',
    'Beth9317': 'cH93KrxN46KnnJET',
    'Cammie7926': 'gtPfaF6g46DNqP7C',
    'Dom6279': '5a8gHqXKhJaEr5in',
    'Eric6099': 'FKk7eqkP5M4Mxi54',
    'Fabian5778': 'CfPocFbm6sLy5qkT',
    'Gemma7450': '9y7i3bTDGfzgPeiS',
    'Harriett4952': '53JCprcsHKFJbNPh',
    'Imogen4248': 'G5Cjk74Q67jtmSg7',
    'Jack1471': 'LJ7sLJQbsTqFkMDs'
}


# Sets the flag to a specific user's password
# TODO Potentially consider randomising the user if I have time
flag_2_user = 'Fabian5778'
flag_2 = users[flag_2_user]


@task2_bp.route('/task2/main')
def main2():

    resp = make_response()
    resp.set_data(render_template('/task2/main2.html'))

    # Clears all the task cookies when the user return to the main page
    for dictuser, dictpass in users.items():
        resp.set_cookie(dictuser, '', expires=0)

    return resp


@task2_bp.route('/task2/info')
def info2():
    return render_template('task2/info2.html')


@task2_bp.route('/task2/login', methods=['GET', 'POST'])
def login2():
    error = ''
    resp = make_response()  # Create a blank response to attach the cookie

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username in users and users[username] == password:
            session['username'] = username
            session['password'] = password

            resp = make_response(redirect(url_for('task2.dashboard2')))
            return resp
        else:
            error = "Invalid credentials for user " + username

    # Renders the login page view and sets the error message
    resp.set_data(render_template('/task2/login2.html', error=error))

    # For each user, creatures a cookie with the name being their username, and their password being the cookie value
    # This is intentionally super vulnerable, as this task is meant to teach users about the basics of utilising a XSS
    # Injection to gain access to a sessions cookies
    for dictuser, dictpass in users.items():
        resp.set_cookie(dictuser, dictpass)
    return resp


@task2_bp.route('/task2/dashboard')
def dashboard2():

    # Redirects the user to the login page if there's no username in the session
    if 'username' not in session:
        return redirect(url_for('task2.login2'))
    username = session['username']

    # Returns a very simple HTML template and the user's username, it doesn't utilise a template
    return render_template_string('''
        <h1>Welcome, {{ username|safe }}!</h1>
        <p>This page is vulnerable to XSS if the username contains malicious code.</p>
        <p><a href="{{ url_for('task2.logout2') }}">Logout</a></p>
    ''', username=username)


@task2_bp.route('/task2/logout')
def logout2():

    # Clears the session and then redirects the user back to the login page
    session.clear()
    return redirect(url_for('task2.login2'))


@task2_bp.route('/task2/register', methods=['GET', 'POST'])
def register2():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Basic validation
        if not username or not password:
            message = "Username and password are required."
        elif username in users:
            message = "Username already exists."
        else:
            # Add the new user account to the dictionary
            users[username] = password
            message = "Registration successful! Please log in."
            return redirect(url_for('task2.login2'))

    return render_template_string('''
        <h2>Register</h2>
        <form method="post">
            Username: <input type="text" name="username" /><br/>
            Password: <input type="password" name="password" /><br/>
            <input type="submit" value="Register" />
        </form>
        <p style="color: red;">{{ message }}</p>
        <p>Already have an account? <a href="{{ url_for('task2.login2') }}">Login here</a>.</p>
    ''', message=message)


@task2_bp.route('/task2/quiz', methods=['GET', 'POST'])
def quiz2():
    return render_template('/task2/quiz2.html')


@task2_bp.route('/task2/answer', methods=['POST'])
def answer2():
    correct_answer = flag_2
    user_answer = request.form.get("answer", "")

    is_correct = user_answer == correct_answer

    return render_template("/task2/answer2.html", is_correct=is_correct)
