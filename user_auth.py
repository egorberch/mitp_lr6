"""Задание №3 (повышенной сложности): Авторизация пользователя."""

import functools
import sys
from typing import Any, Callable, Dict, Optional
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    Response,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "mitp-lr6-variant3-secret-key-super-secure"

# Хранилище пользователей в оперативной памяти (логин -> хэш пароля)
USERS_DB: Dict[str, str] = {
    "admin": generate_password_hash("AdminPass123!"),
}


def login_required(view_func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для ограничения доступа неавторизованным пользователям."""

    @functools.wraps(view_func)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if "username" not in session:
            flash(
                "Для доступа к данной странице необходимо авторизоваться.",
                "info",
            )
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return decorated_function


@app.route("/")
def index() -> Response:
    """Перенаправление с корневого адреса в кабинет или на форму входа."""
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register() -> Any:
    """Регистрация нового пользователя с проверкой пароля и хэшированием."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if len(username) < 3:
            flash("Длина логина должна быть не менее 3 символов.", "danger")
            return render_template("register.html"), 400

        if len(password) < 6:
            flash("Длина пароля должна быть не менее 6 символов.", "danger")
            return render_template("register.html"), 400

        if password != confirm:
            flash("Введенные пароли не совпадают.", "danger")
            return render_template("register.html"), 400

        if username in USERS_DB:
            flash("Пользователь с таким именем уже существует.", "danger")
            return render_template("register.html"), 400

        # Сохранение хэшированного пароля с криптографической солью
        USERS_DB[username] = generate_password_hash(password)
        flash(
            f"Учётная запись '{username}' успешно создана! Войдите в систему.",
            "success",
        )
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> Any:
    """Аутентификация пользователя и открытие сессии."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        password_hash: Optional[str] = USERS_DB.get(username)

        if password_hash and check_password_hash(password_hash, password):
            session.clear()
            session["username"] = username
            flash(f"Добро пожаловать, {username}!", "success")
            return redirect(url_for("dashboard"))

        flash("Неверное имя пользователя или пароль.", "danger")
        return render_template("login.html"), 401

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard() -> str:
    """Защищённый личный кабинет, доступный только авторизованным."""
    current_user = session.get("username", "")
    return render_template("dashboard.html", username=current_user)


@app.route("/logout")
def logout() -> Response:
    """Завершение сеанса пользователя и очистка cookie-сессии."""
    user = session.pop("username", None)
    session.clear()
    if user:
        flash(f"Сеанс пользователя '{user}' успешно завершён.", "info")
    return redirect(url_for("login"))


def main() -> None:
    """Демонстрация полного жизненного цикла системы авторизации."""
    print("=== Демонстрация задания №3 (повыш.): Авторизация пользователя ===")

    with app.test_client() as client:
        # 1. Попытка неавторизованного доступа к закрытому маршруту
        res_guest = client.get("/dashboard")
        print(f"1. Доступ к /dashboard гостем -> HTTP {res_guest.status_code}")
        assert res_guest.status_code == 302, "Ожидался редирект на вход"
        assert "/login" in res_guest.headers.get("Location", "")
        print("   [+] Неавторизованный запрос перенаправлен на /login")

        # 2. Регистрация нового пользователя
        res_reg = client.post(
            "/register",
            data={
                "username": "egor_berchenev",
                "password": "SecurePassword2026",
                "confirm_password": "SecurePassword2026",
            },
        )
        print(f"2. Регистрация аккаунта -> HTTP {res_reg.status_code}")
        assert res_reg.status_code == 302, "Ошибка редиректа регистрации"
        assert "egor_berchenev" in USERS_DB, "Пользователь не добавлен в БД"
        stored_hash = USERS_DB["egor_berchenev"]
        is_hashed = (
            stored_hash.startswith("scrypt:")
            or stored_hash.startswith("pbkdf2:")
        )
        assert is_hashed, "Пароль не захеширован!"
        print("   [+] Пользователь зарегистрирован с хэшированием пароля")

        # 3. Попытка входа с некорректным паролем
        res_bad_login = client.post(
            "/login",
            data={"username": "egor_berchenev", "password": "WrongPassword"},
        )
        print(
            f"3. Вход с неверным паролем -> "
            f"HTTP {res_bad_login.status_code}"
        )
        assert res_bad_login.status_code == 401, "Неверный пароль не отклонен"
        print("   [+] Неверный пароль успешно отклонен сервером")

        # 4. Успешный вход в систему
        res_ok_login = client.post(
            "/login",
            data={
                "username": "egor_berchenev",
                "password": "SecurePassword2026",
            },
        )
        print(f"4. Корректный вход -> HTTP {res_ok_login.status_code}")
        assert res_ok_login.status_code == 302, "Ошибка входа"
        assert "/dashboard" in res_ok_login.headers.get("Location", "")
        print("   [+] Авторизация подтверждена, сессия создана")

        # 5. Доступ к личному кабинету с активной сессией
        res_dash = client.get("/dashboard")
        print(f"5. Доступ к /dashboard -> HTTP {res_dash.status_code}")
        assert res_dash.status_code == 200, "Доступ к кабинету не предоставлен"
        assert "egor_berchenev" in res_dash.get_data(as_text=True)
        print("   [+] Личный кабинет отображает данные пользователя")

        # 6. Выход из системы
        res_logout = client.get("/logout")
        print(f"6. Выход из системы (logout) -> HTTP {res_logout.status_code}")
        assert res_logout.status_code == 302
        res_after = client.get("/dashboard")
        assert res_after.status_code == 302, "Сессия не сброшена"
        print("   [+] Сессия успешно очищена")

    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("\nЗапуск веб-сервера на http://127.0.0.1:5003 ...")
        app.run(host="127.0.0.1", port=5003, debug=True)
    else:
        print(
            "\nДля запуска локального сервера выполните: "
            "python user_auth.py --serve"
        )


if __name__ == "__main__":
    main()
