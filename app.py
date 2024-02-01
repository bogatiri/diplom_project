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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import smtplib
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
import logging


app = Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app)

first_db_connect()
db_session = Session()


app.config['AVATARS_FOLDER'] = 'static/avatars'

app.secret_key = "qeasdqwe"

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


# ----------------------------------------------------------------------------------------------------
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()

message="zdarova pidor!"

@app.route("/send_mail", methods=["POST", "GET"])  #!Отправка письма
def send_email(recipient):
    sender ="ro4evalex@gmail.com"
    password="pkrm pzdv cowo rjxu"
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    
    try:
        server.login(sender, password)
        server.sendmail(sender, recipient,f"Subject: ZDAROVA ZAEBAL!\n{message}" )
        return "Письмо отправлено"
    except Exception as e:
        return "Ошибка авторизации"
    


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
        if not (
            2 <= len(name) <= 90
            and 3 <= len(surname) <= 50
            and 3 <= len(email) <= 50
            and 3 <= len(password) <= 50
            # and 1 <= len(organization) <= 50
            # and 3 <= len(qualification) <= 50
        ):
            return "Недопустимые длины полей"
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
        recipient = email
        send_email(recipient)
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
            user_data = get_user_data(new_user.email)
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
        if user.sections:
            sorted_sections = sorted(user.sections, key=lambda section: section.id)
            for section in sorted_sections:
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

        user = db_session.query(Users).filter_by(email=email_log).first()
        if user and bcrypt.check_password_hash(user.password, password_log):
            user_data = get_user_data(user.email)
            session.update(user_data)
            response = make_response(render_template("main.html", user_data=user_data))
            response.set_cookie("user", user.email, max_age=3600 * 24, path="/")

            return response
        else:
            return "Неверная почта или пароль. Попробуйте снова."
    elif request.method == "GET":
        return render_template("login.html")
#recipient = email_log
#send_mail(recipient) 
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
        user_data = get_user_data(user.email)
        session.update(user_data)
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

    avatar = request.files['avatar']
    user_email = request.cookies.get("user")
    if avatar.filename == '':
        return redirect(request.url)
    if avatar:
        avatar_path = os.path.join(app.config['AVATARS_FOLDER'], avatar.filename)
        avatar.save(avatar_path)
        user = db_session.query(Users).filter_by(email=user_email).first()
        try:
            user.avatar = 'avatars/' + avatar.filename
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print(f"Error: {e}")
        user_data = get_user_data(user.email)
        session.update(user_data)
        response = make_response(render_template("main.html", user_data=user_data))
        response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
        return response
    else:
        return render_template("main.html")

# ----------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------

@app.route('/add_section', methods=['POST'])
def add_section():
    try:
        section_name = request.form.get('section_name')
        user_email = request.cookies.get('user')

        user = db_session.query(Users).filter_by(email=user_email).first()
        if user:
            section = db_session.query(Section).filter_by(user=user, name_of_section=section_name).first()
            if not section:
                section = Section(name_of_section=section_name, user=user)
                db_session.add(section)
                db_session.commit()
                return jsonify({"status": "success", "section_id": section.id, "section_name": section.name_of_section})
            else:
                return jsonify({"status": "error", "message": "Section with this name already exists"})
        else:
            return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------------------------------------------------------------------------------

@app.route('/add_task', methods=['POST'])
def add_task():
    if db_session.is_active:
        print("Сессия активна")
    else:
        print("Сессия закрыта")

    try:
        if request.method == 'POST':
            task_description = request.form.get('task_description')
            section_id = request.form.get('section_id')
            user_email = request.cookies.get('user')
            user = db_session.query(Users).filter_by(email=user_email).first()
            if user:
                section = db_session.query(Section).filter_by(id=section_id).first()
                if not section:
                    return jsonify({"status": "error", "message": "Section not found"})
                new_task = Tasks(task_description=task_description, section=section)
                db_session.add(new_task)
                db_session.commit()
                return jsonify({"status": "success", "task_id": new_task.id})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------------------------------------------------------------------------------

@app.route('/update_task', methods=['POST'])
def update_task():
    try:
        if request.method == 'POST':
            task_id = request.form.get('task_id')
            task_description = request.form.get('task_description')
            task_checked = str2bool(request.form.get('task_checked'))  # Получаем новое значение checked
            user_email = request.cookies.get('user')
            
            user = db_session.query(Users).filter_by(email=user_email).first()
            if user:
                task = db_session.query(Tasks).filter_by(id=task_id).first()
                if not task:
                    return jsonify({"status": "error", "message": "Task not found"})
                task.task_description = task_description
                task.checked = task_checked  # Обновляем значение checked
                db_session.commit()
                return jsonify({"status": "success", "task_id": task.id, "task_description": task.task_description, "task_checked": task.checked})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------------------------------------------------------------------------------

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
                return jsonify({"status": "success", "message": "Task deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------------------------------------------------------------------------------

@app.route('/get_sections')
def get_sections():
    try:
        user_email = request.cookies.get('user')
        
        user = db_session.query(Users).filter_by(email=user_email).first()
        if user:
            sections = db_session.query(Section).filter_by(user=user).order_by(Section.id).all()
            sections_json = [{
                "id": section.id,
                "name_of_section": section.name_of_section} for section in sections]
            return jsonify(sections_json)
        else:
            return jsonify({"status": "error", "message": "User not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------------------------------------------------------------------------------

logging.basicConfig(filename='app.log', level=logging.INFO)

# !Маршрут для получения списка задач для указанной секции
@app.route('/get_tasks')
def get_tasks():
    try:
        section_id = request.args.get('sectionId')
        logging.info(f"Getting tasks for section_id: {section_id}")
        try:
            tasks = db_session.query(Tasks).filter_by(section_id=section_id).order_by(Tasks.id).all()
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            raise
        logging.info(f"Got {len(tasks)} tasks")
        tasks_json = [
            {
                "id": task.id,
                "task_description": task.task_description,  # Добавьте проверку на None
                "checked": task.checked
            } for task in tasks
        ]
        logging.info(f"Tasks data: {tasks_json}")
        response = jsonify({"tasks": tasks_json})
        logging.info(f"Response ready: {response}")
        return response
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


# ----------------------------------------------------------------------------------------------------

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
    user_email = request.cookies.get("user")
    save_theme_to_db(theme, user_email)
    return "Theme saved successfully!"

# ----------------------------------------------------------------------------------------------------

@app.route("/logout")  #!Выход
def logout():
    response = make_response(redirect(url_for("login_form")))
    response.delete_cookie("user")
    alert_script = '<script>alert("Вы успешно вышли!");</script>'
    response.set_data(response.get_data(as_text=True) + alert_script)
    return response

# ----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)