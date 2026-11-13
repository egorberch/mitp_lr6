"""Задание №5 (средней сложности): Страница с Bootstrap."""

import sys
from typing import Any, Dict, List
from flask import Flask, jsonify, render_template, Response

app = Flask(__name__, template_folder="templates")

TECH_STACK: List[Dict[str, str]] = [
    {
        "name": "Bootstrap 5",
        "category": "Frontend",
        "description": "Популярный CSS-фреймворк с адаптивной сеткой,"
        " готовыми UI-компонентами и утилитами.",
        "status": "Подключено",
        "badge_class": "bg-success",
        "version": "v5.3.3",
    },
    {
        "name": "Flask",
        "category": "Backend",
        "description": "Легковесный WSGI веб-фреймворк на Python для быстрого"
        " создания надежных приложений и REST API.",
        "status": "Активно",
        "badge_class": "bg-primary",
        "version": "v3.0+",
    },
    {
        "name": "Jinja2",
        "category": "Шаблонизатор",
        "description": "Скоростной и безопасный движок шаблонов с поддержкой"
        " наследования, макросов и фильтров.",
        "status": "Используется",
        "badge_class": "bg-info text-dark",
        "version": "v3.1+",
    },
]

TASKS_TABLE: List[Dict[str, Any]] = [
    {
        "num": 1,
        "level": "Средняя",
        "level_badge": "bg-secondary",
        "title": "Статическая страница + CSS (Задание 3)",
        "script": "static_page.py",
    },
    {
        "num": 2,
        "level": "Средняя",
        "level_badge": "bg-secondary",
        "title": "Страница с Bootstrap (Задание 5)",
        "script": "bootstrap_page.py",
    },
    {
        "num": 3,
        "level": "Средняя",
        "level_badge": "bg-secondary",
        "title": "Шаблон Jinja2 с данными (Задание 9)",
        "script": "jinja_template.py",
    },
    {
        "num": 4,
        "level": "Повышенная",
        "level_badge": "bg-warning text-dark",
        "title": "Авторизация пользователя (Задание 3)",
        "script": "user_auth.py",
    },
    {
        "num": 5,
        "level": "Повышенная",
        "level_badge": "bg-warning text-dark",
        "title": "Деплой на Heroku (Задание 7)",
        "script": "heroku_deploy.py",
    },
]


@app.route("/")
def index() -> str:
    """Отображение адаптивной страницы с интерфейсом Bootstrap 5."""
    return render_template(
        "bootstrap_page.html",
        title="Адаптивная страница на Bootstrap 5 | МИТП ЛР6",
        tech_stack=TECH_STACK,
        tasks_table=TASKS_TABLE,
    )


@app.route("/api/technologies")
def get_technologies() -> Response:
    """REST endpoint, возвращающий список технологий в JSON-формате."""
    return jsonify({"count": len(TECH_STACK), "items": TECH_STACK})


def main() -> None:
    """Демонстрация работы адаптивной страницы с Bootstrap 5."""
    print("=== Демонстрация задания №5: Страница с Bootstrap ===")

    with app.test_client() as client:
        # Тестирование рендеринга страницы
        res_page = client.get("/")
        print(f"GET / -> Код ответа: {res_page.status_code}")
        assert res_page.status_code == 200, "Ошибка загрузки страницы"
        html = res_page.get_data(as_text=True)
        assert "bootstrap.min.css" in html, "Bootstrap CSS не подключен"
        assert "bootstrap.bundle.min.js" in html, "Bootstrap JS не подключен"
        assert "navbar" in html, "Компонент Navbar отсутствует в разметке"
        assert "modal" in html, "Компонент Modal отсутствует в разметке"
        print("  [+] Bootstrap 5 успешно подключен и компоненты сформированы")

        # Тестирование JSON-эндпоинта
        res_api = client.get("/api/technologies")
        print(f"GET /api/technologies -> Код ответа: {res_api.status_code}")
        assert res_api.status_code == 200, "Ошибка API технологий"
        data = res_api.get_json()
        assert data["count"] == 3, "Неверное количество технологий в ответе"
        print("  [+] API данных успешно возвращает JSON-структуру")

    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("\nЗапуск веб-сервера на http://127.0.0.1:5001 ...")
        app.run(host="127.0.0.1", port=5001, debug=True)
    else:
        print(
            "\nДля запуска локального сервера выполните: "
            "python bootstrap_page.py --serve"
        )


if __name__ == "__main__":
    main()
