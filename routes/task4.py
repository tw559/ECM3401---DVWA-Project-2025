from flask import Blueprint, request, render_template

task4_bp = Blueprint('task4', __name__)


@task4_bp.route('/task4/main')
def main4():
    return render_template('/task4/main4.html')


@task4_bp.route('/task4/info')
def info4():
    return render_template('/task4/info4.html')


# This route does not actually pass an error. Rather, it passes the template for a page that looks like an error for
# the task
@task4_bp.route('/task4/login')
def ferror4():
    return render_template('/task4/ferror4.html')


@task4_bp.route('/task4/admin')
@task4_bp.route('/task4/admin/home')
def admin4_home():
    return render_template('/task4/admin4_home.html')


users = {
    93015813: {'username': 'Alice9774', 'email': 'alice9774@dvwa.com', 'role': 'User', 'address': '63 Avispa Road'},
    21033058: {'username': 'Bob4444', 'email': 'bob4444@dvwa.com', 'role': 'User', 'address': '21 Casper Street'},
    23723044: {'username': 'Charlie6866', 'email': 'charlie6866@dvwa.com', 'role': 'Moderator', 'address': '18 Squirrel Road'},
    10369333: {'username': 'Dave2273', 'email': 'dave2273@dvwa.com', 'role': 'User', 'address': '5 Scyther Crescent'},
    47990229: {'username': 'Eve1046', 'email': 'eve1046@dvwa.com', 'role': 'User', 'address': '9 Maude Road'},
    49667977: {'username': 'Felix9486', 'email': 'felix9486@dvwa.com', 'role': 'User', 'address': '32 Tamarin Road'},
}


@task4_bp.route('/task4/admin/users')
def admin4_users():
    return render_template('/task4/admin4_users.html', users=users)


@task4_bp.route('/task4/dashboard/<int:user_id>')
def dashboard(user_id):
    if user_id not in users:
        return "User not found", 404
    user = users[user_id]
    return render_template('/task4/dashboard4.html', user=user, user_id=user_id)


flag_4 = users[23723044]['address']


@task4_bp.route('/task4/quiz', methods=['GET', 'POST'])
def quiz4():
    return render_template('/task4/quiz4.html')


@task4_bp.route('/task4/answer', methods=['POST'])
def answer4():
    correct_answer = flag_4
    user_answer = request.form.get("answer", "")

    is_correct = user_answer == correct_answer

    return render_template("/task4/answer4.html", is_correct=is_correct)
