"""
This file contains the main code for the To-Do list application.

The code is structured as a series of functions and routes, each of which performs a specific task.

The functions are designed to be modular and reusable, allowing for easy maintenance and modification of the application.

The routes are defined using the Flask framework, and map requests to specific functions.

The code uses a relational database to store user information, task lists, and other data.

Overall, the code is designed to be user-friendly, with a clean and intuitive interface."""

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    make_response,
    url_for,
    session,
    jsonify
)
from src.db.models import Users, Section, Tasks
from src.db.connect import Session, first_db_connect
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app)

first_db_connect()
db_session = Session()

app.config['AVATARS_FOLDER'] = 'static/avatars'

app.secret_key = "qeasdqwe"

# ----------------------------------------------------------------------------------------------------


@app.route("/", methods=["POST", "GET"])  #!Регистрация
def register_form():
    if request.method == "POST":
        name = request.form.get("name-reg")
        surname = request.form.get("surname")
        email = request.form.get("email-reg")
        password = request.form.get("password-reg")
        organization = request.form.get("organization-reg")
        qualification = request.form.get("qualification")

        # Проверка длины полей
        if not (
            2 <= len(name) <= 90
            and 3 <= len(surname) <= 50
            and 3 <= len(email) <= 50
            and 3 <= len(password) <= 50
            and 1 <= len(organization) <= 50
            and 3 <= len(qualification) <= 50
        ):
            return "Недопустимые длины полей"

        # Хэшируем пароль
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        existing_user = db_session.query(Users).filter_by(email=email).first()

        if existing_user:
            return "User with this email already exists. Please choose another email."

        new_user = Users(
            name=name,
            surname=surname,
            email=email,
            password=hashed_password,
            organization=organization,
            qualification=qualification,
        )

        try:
            db_session.add(new_user)
            db_session.commit()

            existing_section = db_session.query(Section).filter_by(name_of_section="Default Section", user=new_user).first()

            if not existing_section:
                new_section = Section(name_of_section="Default Section", user=new_user)
                db_session.add(new_section)
                db_session.commit()
            else:
                new_section = existing_section

            # Получите данные пользователя
            user_data = get_user_data(new_user.email)

            # Передайте данные пользователя в шаблон
            return render_template("login.html", user_data=user_data)

        except IntegrityError:
            db_session.rollback()
            return "User already exists in the database!"

    elif request.method == "GET":
        return render_template("login.html", user_data={})


# ----------------------------------------------------------------------------------------------------



def get_user_data(email):
    user = db_session.query(Users).filter_by(email=email).first()
    if user:
        user_data = {
            "user_theme": user.theme,
            "user_name": user.name,
            "user_surname": user.surname,
            "user_qualification": user.qualification,
            "user_about": user.about,
            "user_avatar": user.avatar,
            "sections": []
        }

        # Если у пользователя есть связанные секции, добавьте их данные
        if user.sections:
            for section in user.sections:
                section_data = {
                    "name_of_section": section.name_of_section,
                    "section_id": section.id
                }
                user_data["sections"].append(section_data)

        return user_data

    return {}

# ----------------------------------------------------------------------------------------------------


@app.route("/login_form", methods=["POST", "GET"])  #!Авторизация
def login_form():
    if request.method == "POST":
        email_log = request.form.get("email-log")
        password_log = request.form.get("password-log")

        # Извлекаем пользователя из базы данных по введенной почте
        user = db_session.query(Users).filter_by(email=email_log).first()

        if user and bcrypt.check_password_hash(user.password, password_log):
                # Обновление сессии
            user_data = get_user_data(user.email)
            session.update(user_data)

            # Создаем объект response и устанавливаем куки
            response = make_response(render_template("main.html", user_data=user_data))
            response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
            return response
        else:
            # Неверные почта или пароль
            return "Неверная почта или пароль. Попробуйте снова."
    elif request.method == "GET":
        return render_template("login.html")


# ----------------------------------------------------------------------------------------------------


def get_user_pass(user_email):  #!Получение пароля пользователя
    user = db_session.query(Users).filter_by(email=user_email).first()
    return user.password if user else None


# ----------------------------------------------------------------------------------------------------


@app.route("/pass_switch", methods=["POST", "GET"])  #!Смена пароля
def pass_switch():
    if request.method == "POST":
        password_old = request.form.get("password-old")
        password_new = request.form.get("password-new")
        password_new_repeated = request.form.get("password-new-repeated")
        user_email = request.cookies.get("user")

        user = db_session.query(Users).filter_by(email=user_email).first()

        if user and bcrypt.check_password_hash(user.password, password_old):
            if password_new == password_new_repeated:
                hashed_password_new = bcrypt.generate_password_hash(
                    password_new
                ).decode("utf-8")
                user.password = hashed_password_new

                db_session.commit()

                # Обновление сессии
                user_data = get_user_data(user.email)
                session.update(user_data)

                response = make_response(render_template("main.html", user_data=user_data))
                response.set_cookie("user", user.email, max_age=3600 * 24, path="/")

                return response
            else:
                return "Новые пароли не совпадают."
        else:
            return "Неверный текущий пароль. Пароль не изменен."
    else:
        return render_template("main.html", **user_data)


# ----------------------------------------------------------------------------------------------------


@app.route("/about_info", methods=["POST", "GET"])  #!Смена данных пользователя
def about_info():
    if request.method == "POST":
        name_new = request.form.get("name-new")
        surname_new = request.form.get("surname-new")
        about = request.form.get("about")
        user_email = request.cookies.get("user")

        user = db_session.query(Users).filter_by(email=user_email).first()

        user.name = name_new
        user.surname = surname_new
        user.about = about

        db_session.commit()

    # Обновление сессии
        user_data = get_user_data(user.email)
        session.update(user_data)

        # Создаем объект response и устанавливаем куки
        response = make_response(render_template("main.html", user_data=user_data))
        response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
        return response

    else:
        return render_template("main.html")


#----------------------------------------------------------------------------------------------------


@app.route('/upload_avatar', methods=['POST', 'GET']) #!Функция загрузки аватара
def upload_avatar():
    if 'avatar' not in request.files:
        return redirect(request.url)

    avatar = request.files['avatar']  # Чтение данных изображения
    user_email = request.cookies.get("user")

    if avatar.filename == '':
        return redirect(request.url)

    if avatar:
        # Сохраняем аватар в директории AVATARS_FOLDER
        avatar_path = os.path.join(app.config['AVATARS_FOLDER'], avatar.filename)
        avatar.save(avatar_path)

        user = db_session.query(Users).filter_by(email=user_email).first()

        try:
            user.avatar = 'avatars/' + avatar.filename
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print(f"Error: {e}")

            # Обновление сессии
        user_data = get_user_data(user.email)
        session.update(user_data)

        # Создаем объект response и устанавливаем куки
        response = make_response(render_template("main.html", user_data=user_data))
        response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
        return response
    else:
        return render_template("main.html")


# ----------------------------------------------------------------------------------------------------
@app.route('/add_section', methods=['POST'])
def add_section():
    try:
        section_name = request.form.get('section_name')

        # Получаем пользователя из куков
        user_email = request.cookies.get('user')
        user = db_session.query(Users).filter_by(email=user_email).first()

        if user:
            # Проверяем, существует ли секция с указанным именем для данного пользователя
            section = db_session.query(Section).filter_by(user=user, name_of_section=section_name).first()

            # Если секция не существует, создаем новую секцию
            if not section:
                section = Section(name_of_section=section_name, user=user)
                db_session.add(section)
                db_session.commit()

                return jsonify({"status": "success", "section_id": section.id})
            else:
                return jsonify({"status": "error", "message": "Section with this name already exists"})
        else:
            return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/save_name_of_section', methods=['POST'])
def save_name_of_section():
    if request.method == 'POST':
        name_of_section = request.form.get('text')
        section_id = request.form.get('section_id')
        user_email = request.cookies.get('user')
        user = db_session.query(Users).filter_by(email=user_email).first()
        if user:
            section = db_session.query(Section).filter_by(user=user, id=section_id).first()
            if section:
                section.name_of_section = name_of_section
                db_session.commit()

                return 'Success', 200
            else:
                return 'Section not found', 404
        else:
            return 'User not found', 404


@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        if request.method == 'POST':
            task_description = request.form.get('task_description')

            user_email = request.cookies.get('user')
            user = db_session.query(Users).filter_by(email=user_email).first()

            if user:
                section = db_session.query(Section).filter_by(user=user).first()

                if not section:
                    return jsonify({"status": "error", "message": "Section not found"})

                new_task = Tasks(task_description=task_description, section=section)
                db_session.add(new_task)
                db_session.commit()

                # Возвращаем успешный статус и идентификатор задачи
                return jsonify({"status": "success", "task_id": new_task.id})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/update_task', methods=['POST'])
def update_task():
    try:
        if request.method == 'POST':
            task_id = request.form.get('task_id')
            task_description = request.form.get('task_description')

            user_email = request.cookies.get('user')
            user = db_session.query(Users).filter_by(email=user_email).first()

            if user:
                task = db_session.query(Tasks).filter_by(id=task_id).first()

                if not task:
                    return jsonify({"status": "error", "message": "Task not found"})

                task.task_description = task_description
                db_session.commit()

                # Возвращаем успешный статус и идентификатор задачи
                return jsonify({"status": "success", "task_id": task.id, "task_description": task.task_description})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/delete_task', methods=['POST'])
def delete_task():
    try:
        if request.method == 'POST':
            task_id = request.form.get('task_id')

            user_email = request.cookies.get('user')
            user = db_session.query(Users).filter_by(email=user_email).first()

            if user:
                task = db_session.query(Tasks).filter_by(id=task_id).first()

                if not task:
                    return jsonify({"status": "error", "message": "Task not found"})

                db_session.delete(task)
                db_session.commit()

                # Возвращаем успешный статус
                return jsonify({"status": "success", "message": "Task deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/get_sections')
def get_sections():
    try:
        # Получаем пользователя из куков
        user_email = request.cookies.get('user')
        user = db_session.query(Users).filter_by(email=user_email).first()

        if user:
            # Получаем список секций для данного пользователя
            sections = db_session.query(Section).filter_by(user=user).all()

            # Преобразуем секции в формат JSON
            sections_json = [{"id": section.id, "name_of_section": section.name_of_section} for section in sections]

            return jsonify(sections_json)
        else:
            return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
# ----------------------------------------------------------------------------------------------------
# !Маршрут для получения списка задач для указанной секции
@app.route('/get_tasks')
def get_tasks():
    try:
        section_id = request.args.get('sectionId')  # Исправлено на 'sectionId'

        # Получаем задачи для указанной секции
        tasks = db_session.query(Tasks).filter_by(section_id=section_id).all()

        # Преобразуем задачи в формат JSON
        tasks_json = [
            {
                "id": task.id,
                "task_description": task.task_description if task.task_description else '',  # Добавьте проверку на None
                "checked": task.checked
            } for task in tasks
        ]
        return jsonify({"tasks": tasks_json})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def save_theme_to_db(theme, user_email):  #!Функция сохранения темы
    try:
        user = db_session.query(Users).filter_by(email=user_email).first()

        if user:
            user.theme = theme
            db_session.commit()
            print("Тема успешно сохранена")
        else:
            print("Пользователь не найден")

    except Exception as e:
        db_session.rollback()
        print(f"Ошибка при сохранении темы: {e}")


# ----------------------------------------------------------------------------------------------------


@app.route("/save_theme", methods=["POST"])  #!Сохранение темы
def save_theme():
    theme = request.form.get("theme")
    user_email = request.cookies.get("user")  # Получаем email пользователя из куки

    save_theme_to_db(theme, user_email)

    return "Theme saved successfully!"


# ----------------------------------------------------------------------------------------------------


@app.route("/logout")  #!Выход
def logout():
    # Удаляем куки пользователя
    response = make_response(redirect(url_for("login_form")))
    response.delete_cookie("user")

    # Выводим сообщение с использованием JavaScript
    alert_script = '<script>alert("Вы успешно вышли!");</script>'
    response.set_data(response.get_data(as_text=True) + alert_script)

    return response


# ----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
