"""Задание №7 (повышенной сложности): Деплой на Heroku."""

import datetime
import os
import sys
from typing import Any, Dict
from flask import Flask, jsonify, render_template, Response

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "heroku-default-dev-secret-key"
)


@app.route("/")
def index() -> str:
    """Главная страница приложения с информацией о конфигурации Heroku."""
    meta: Dict[str, Any] = {
        "platform": "Heroku Cloud Application",
        "wsgi_server": "Gunicorn 21.2+",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "environment": os.environ.get("FLASK_ENV", "production"),
        "port": os.environ.get("PORT", "5000"),
    }
    return render_template("heroku.html", meta=meta)


@app.route("/health")
def health() -> Response:
    """Healthcheck эндпоинт для мониторинга работоспособности сервиса."""
    payload: Dict[str, Any] = {
        "status": "UP",
        "platform": "Heroku",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "procfile_command": "gunicorn heroku_deploy:app",
    }
    return jsonify(payload)


def verify_deployment_files() -> None:
    """Проверка наличия необходимых конфигурационных файлов деплоя."""
    procfile_path = "Procfile"
    runtime_path = "runtime.txt"
    reqs_path = "requirements.txt"

    print("Проверка файлов деплоя на Heroku:")
    for path in (procfile_path, runtime_path, reqs_path):
        exists = os.path.isfile(path)
        status = "[+] НАЙДЕН" if exists else "[-] ОТСУТСТВУЕТ"
        print(f"  {status}: {path}")
        assert exists, f"Файл деплоя {path} не найден!"

    with open(procfile_path, "r", encoding="utf-8") as file:
        procfile_content = file.read().strip()
        assert "gunicorn" in procfile_content, "Procfile без gunicorn"
        assert "heroku_deploy:app" in procfile_content, (
            "Procfile должен ссылаться на heroku_deploy:app"
        )
        print("  [+] Конфигурация Procfile корректна")


def main() -> None:
    """Демонстрация готовности к деплою на Heroku и проверка API."""
    print("=== Демонстрация задания №7 (повыш.): Деплой на Heroku ===")

    # 1. Проверка конфигурационных файлов репозитория
    verify_deployment_files()

    # 2. Тестирование веб-сервера через test_client
    with app.test_client() as client:
        res_index = client.get("/")
        print(f"\nGET / -> Код ответа: {res_index.status_code}")
        assert res_index.status_code == 200, "Ошибка главной страницы"
        print("  [+] Главная страница приложения успешно отрендерена")

        res_health = client.get("/health")
        print(f"GET /health -> Код ответа: {res_health.status_code}")
        assert res_health.status_code == 200, "Ошибка healthcheck"
        health_data = res_health.get_json()
        assert health_data["status"] == "UP", "Неверный статус healthcheck"
        print(
            f"  [+] Эндпоинт здоровья подтвердил статус: "
            f"{health_data['status']}"
        )

    # 3. Инструкции по публикации
    port = int(os.environ.get("PORT", 5000))
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print(f"\nЗапуск сервера на порту {port}...")
        app.run(host="0.0.0.0", port=port, debug=False)
    else:
        print("\nКоманды деплоя на Heroku:")
        print("  1. heroku login")
        print("  2. heroku create mitp-lr6-app")
        print("  3. git push heroku main")
        print("  4. heroku open")
        print(
            "\nДля локального запуска выполните: "
            "python heroku_deploy.py --serve"
        )


if __name__ == "__main__":
    main()
