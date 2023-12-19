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

app = Flask(__name__)
bcrypt = Bcrypt(app)

first_db_connect()
db_session = Session()

app.secret_key = "qeasdqwe"

#----------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------

def get_user_theme(user_email):
    user = db_session.query(Users).filter_by(email=user_email).first()
    return user.theme, user.name, user.surname, user.qualification if user else None

#----------------------------------------------------------------------------------------------------

@app.route("/login_form", methods=["POST", "GET"])  #!Авторизация
def login_form():
    if request.method == "POST":
        email_log = request.form.get("email-log")
        password_log = request.form.get("password-log")

        # Извлекаем пользователя из базы данных по введенной почте
        user = db_session.query(Users).filter_by(email=email_log).first()

        if user and bcrypt.check_password_hash(user.password, password_log):
            user_theme, user_name, user_surname, user_qualification = get_user_theme(
                user.email
            )
            session["user_theme"] = user_theme  # Пример для использования сессии
            session["user_name"] = (user_name, user_surname)
            session["user_qualification"] = user_qualification

            response = make_response(
                render_template(
                    "main.html",
                    user_theme=user_theme,
                    user_name=user_name,
                    user_surname=user_surname,
                    user_qualification=user_qualification,
                )
            )
            response.set_cookie("user", user.email, max_age=3600, path="/")
            return response
        else:
            # Неверные почта или пароль
            return "Неверная почта или пароль. Попробуйте снова."
    elif request.method == "GET":
        return render_template("login.html")

#----------------------------------------------------------------------------------------------------

def get_user_pass(user_email):
    user = db_session.query(Users).filter_by(email=user_email).first()
    return user.password if user else None

#----------------------------------------------------------------------------------------------------

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
                ) = get_user_theme(user.email)
                session["user_theme"] = user_theme
                session["user_name"] = (user_name, user_surname)
                session["user_qualification"] = user_qualification

                response = make_response(
                    render_template(
                        "main.html",
                        user_theme=user_theme,
                        user_name=user_name,
                        user_surname=user_surname,
                        user_qualification=user_qualification,
                    )
                )
                response.set_cookie("user", user.email, max_age=3600, path="/")

                return response
            else:
                return "Новые пароли не совпадают."
        else:
            return "Неверный текущий пароль. Пароль не изменен."
    else:
        return render_template("main.html")

#----------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------

@app.route("/save_theme", methods=["POST"])  #!Сохранение темы
def save_theme():
    theme = request.form.get("theme")
    user_email = request.cookies.get("user")  # Получаем email пользователя из куки

    save_theme_to_db(theme, user_email)

    return "Theme saved successfully!"

#----------------------------------------------------------------------------------------------------

@app.route("/logout")  #!Выход
def logout():
    # Удаляем куки пользователя
    response = make_response(redirect(url_for("login_form")))
    response.delete_cookie("user")

    # Выводим сообщение с использованием JavaScript
    alert_script = '<script>alert("Вы успешно вышли!");</script>'
    response.set_data(response.get_data(as_text=True) + alert_script)

    return response

#----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
