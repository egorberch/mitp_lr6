"""Задание №3 (средней сложности): Статическая страница + CSS."""

import sys
from flask import Flask, render_template, Response

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index() -> str:
    """Отображение главной статической страницы с подключением CSS."""
    return render_template(
        "static_page.html",
        title="Статическая страница с CSS | МИТП ЛР6",
        heading="Веб-разработка на Python",
    )


@app.route("/health")
def health() -> Response:
    """Проверка доступности веб-сервиса."""
    return Response("OK", status=200, mimetype="text/plain")


def main() -> None:
    """Демонстрация работы статической страницы и стилей."""
    print("=== Демонстрация задания №3: Статическая страница + CSS ===")

    with app.test_client() as client:
        # Проверка ответа главной страницы
        res_page = client.get("/")
        print(f"GET / -> Код ответа: {res_page.status_code}")
        assert res_page.status_code == 200, "Ошибка загрузки страницы"
        page_html = res_page.get_data(as_text=True)
        assert "style.css" in page_html, "Ссылка на style.css отсутствует"
        print("  [+] Главная страница успешно отдана со ссылкой на CSS")

        # Проверка отдачи статического файла стилей
        res_css = client.get("/static/css/style.css")
        print(
            f"GET /static/css/style.css -> Код ответа: {res_css.status_code}"
        )
        assert res_css.status_code == 200, "Ошибка отдачи static style.css"
        assert "text/css" in res_css.content_type, "Некорректный Content-Type"
        print("  [+] Статический CSS-файл успешно отдан веб-сервером")

    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("\nЗапуск веб-сервера на http://127.0.0.1:5000 ...")
        app.run(host="127.0.0.1", port=5000, debug=True)
    else:
        print(
            "\nДля запуска локального сервера выполните: "
            "python static_page.py --serve"
        )


if __name__ == "__main__":
    main()
