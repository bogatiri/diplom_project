from flask import (
    Flask,
    request,
    render_template,
    redirect,
    make_response,
    url_for,
    session,
)
from src.db.models import Users
from src.db.connect import Session, first_db_connect
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

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
            return render_template("login.html")
        except IntegrityError:
            db_session.rollback()
            return "User already exists in the database!"
    elif request.method == "GET":
        return render_template("login.html")


# ----------------------------------------------------------------------------------------------------


def get_user_data(user_email):  #!Получение данных пользователя
    user = db_session.query(Users).filter_by(email=user_email).first()
    return (
        user.theme,
        user.name,
        user.surname,
        user.qualification,
        user.about,
        user.avatar if user else None,
    )


# ----------------------------------------------------------------------------------------------------


@app.route("/login_form", methods=["POST", "GET"])  #!Авторизация
def login_form():
    if request.method == "POST":
        email_log = request.form.get("email-log")
        password_log = request.form.get("password-log")

        # Извлекаем пользователя из базы данных по введенной почте
        user = db_session.query(Users).filter_by(email=email_log).first()

        if user and bcrypt.check_password_hash(user.password, password_log):
            (
                user_theme,
                user_name,
                user_surname,
                user_qualification,
                user_about,
                user_avatar
            ) = get_user_data(user.email)
            session["user_theme"] = user_theme  # Пример для использования сессии
            session["user_name"] = (user_name, user_surname)
            session["user_qualification"] = user_qualification
            session["user_about"] = user_about
            session["user_avatar"] =user_avatar
            response = make_response(
                render_template(
                    "main.html",
                    user_theme=user_theme,
                    user_name=user_name,
                    user_surname=user_surname,
                    user_qualification=user_qualification,
                    user_about=user_about,
                    user_avatar = user_avatar,
                )
            )
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

                # Обновляем сессию с новой темой
                (
                    user_theme,
                    user_name,
                    user_surname,
                    user_qualification,
                    user_about,
                ) = get_user_data(user.email)
                session["user_theme"] = user_theme
                session["user_name"] = (user_name, user_surname)
                session["user_qualification"] = user_qualification
                session["user_about"] = user_about

                response = make_response(
                    render_template(
                        "main.html",
                        user_theme=user_theme,
                        user_name=user_name,
                        user_surname=user_surname,
                        user_qualification=user_qualification,
                        user_about=user_about,
                    )
                )
                response.set_cookie("user", user.email, max_age=3600 * 24, path="/")

                return response
            else:
                return "Новые пароли не совпадают."
        else:
            return "Неверный текущий пароль. Пароль не изменен."
    else:
        return render_template("main.html")


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

        # Обновляем сессию
        (
            user_theme,
            user_name,
            user_surname,
            user_qualification,
            user_about,
            user_avatar,
        ) = get_user_data(user.email)
        session["user_theme"] = user_theme
        session["user_name"] = (user_name, user_surname)
        session["user_qualification"] = user_qualification
        session["user_about"] = user_about
        session["user_avatar"] = user_avatar
        response = make_response(
            render_template(
                "main.html",
                user_theme = user_theme,
                user_name = user_name,
                user_surname = user_surname,
                user_qualification = user_qualification,
                user_about = user_about,
                user_avatar = user_avatar,
            )
        )
        response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
        return response

    else:
        return render_template("main.html")


#----------------------------------------------------------------------------------------------------


@app.route('/upload_avatar', methods=['POST', 'GET'])
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

        (
                user_theme,
                user_name,
                user_surname,
                user_qualification,
                user_about,
                user_avatar,
        ) = get_user_data(user.email)

        session["user_theme"] = user_theme
        session["user_name"] = (user_name, user_surname)
        session["user_qualification"] = user_qualification
        session["user_about"] = user_about
        session["user_avatar"] = user_avatar

        response = make_response(
                render_template(
                    "main.html",
                    user_theme=user_theme,
                    user_name=user_name,
                    user_surname=user_surname,
                    user_qualification=user_qualification,
                    user_about=user_about,
                    user_avatar=user_avatar,
                )
            )

        response.set_cookie("user", user.email, max_age=3600 * 24, path="/")
        return response
    else:
        return render_template("main.html")


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
