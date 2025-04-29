from flask import Flask, request, redirect, url_for, make_response, render_template
from routes.task1 import task1_bp
from routes.task2 import task2_bp
from routes.task3 import task3_bp
from routes.task4 import task4_bp
from routes.task5 import task5_bp

app = Flask(__name__)
# TODO Change this key to something actually secure
app.secret_key = 'IfIGetAnotherSQLErrorIllScream'


@app.route('/')
def disclaimer():
    """
    The initial page the web application loads to, contains a disclaimer on the usage of the application
    :return: The view for the disclaimer page
    """
    return render_template('disclaimer.html')


@app.route('/index')
def index():
    """
    The main page of the DVWA. Contains the links to each task
    :return: Returns the view for the page
    """
    return render_template('home.html')


@app.route('/test/set_cookie')
def set_cookie():
    """
    A depreciated route, its current usage is to set a cookie for testing purposes
    :return: Redirects the user back to the index page, but sets a cookie as detailed
    TODO Make sure to delete before the final product release
    """
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('my_cookie', '1', max_age=60 * 60 * 24)  # Expires in 1 day
    return resp


@app.route('/test/get_cookie/')
def get_cookie():
    """
    A depreciated route, currently used for testing to check that a cookie has been set
    :return: Returns a view that gives the value of the cookie with the name specified in cookie_value, otherwise
    returns 'No cookie found!'
    TODO Make sure to delete before the final product release
    """
    cookie_value = request.cookies.get('my_cookie')
    if cookie_value:
        return f'Cookie Value: {cookie_value}'
    return 'No cookie found!'


@app.route('/test/open/')
def test_open():
    """
    A depreciated route, redirects the user to the task 1 login page.
    TODO Can probably be deleted, check for dependencies first
    :return:
    """
    return render_template('/task1/login1.html')


"""
Each set registers the route blueprint for each task. Compartmentalising the routes helps reduce any possible 
errors from unexpected interactions, as well as helps to keep the code more readable. If you intend to add any more 
tasks, make sure to specify the blueprint here.
"""
app.register_blueprint(task1_bp)
app.register_blueprint(task2_bp)
app.register_blueprint(task3_bp)
app.register_blueprint(task4_bp)
app.register_blueprint(task5_bp)

if __name__ == '__main__':
    # TODO Set debug to false for final release
    app.run(debug=True)
