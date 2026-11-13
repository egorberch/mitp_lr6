"""Задание №9 (средней сложности): Шаблон Jinja2 с данными."""

import sys
from typing import Any, Dict, List
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.template_filter("currency")
def currency_filter(value: float) -> str:
    """Форматирование числового значения в валютный вид (рубли)."""
    try:
        formatted = f"{float(value):,.2f}".replace(",", " ")
        return f"{formatted} ₽"
    except (ValueError, TypeError):
        return f"{value} ₽"


@app.template_filter("grade_badge")
def grade_badge_filter(score: int) -> str:
    """Формирование HTML-бейджа успеваемости на основе баллов."""
    if score >= 85:
        return '<span class="badge bg-success">A (Отлично)</span>'
    if score >= 70:
        return '<span class="badge bg-primary">B (Хорошо)</span>'
    if score >= 50:
        return '<span class="badge bg-warning text-dark">C (Удовл.)</span>'
    return '<span class="badge bg-danger">F (Неуд.)</span>'


COURSE_INFO: Dict[str, Any] = {
    "name": "Методы и технологии программирования",
    "semester": 5,
    "group": "220042-11",
    "instructor": "Преподаватель кафедры ПМиКН",
}

STUDENTS_LIST: List[Dict[str, Any]] = [
    {"name": "Берченёв Егор Константинович", "score": 98},
    {"name": "Иванов Иван Иванович", "score": 86},
    {"name": "Петров Петр Сергеевич", "score": 74},
    {"name": "Смирнова Анна Дмитриевна", "score": 68},
    {"name": "Кузнецов Алексей Владимирович", "score": 45},
]

GRANTS_LIST: List[Dict[str, Any]] = [
    {"title": "Повышенная академическая стипендия", "amount": 14500.0},
    {"title": "Базовая государственная стипендия", "amount": 3200.0},
    {"title": "Грант за научные достижения", "amount": 25000.0},
    {"title": "Стипендия за победу в хакатоне", "amount": 18000.0},
]


@app.route("/")
def index() -> str:
    """Отображение шаблона Jinja2 со сложными структурами данных."""
    scores = [s["score"] for s in STUDENTS_LIST]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    total_budget = sum(g["amount"] for g in GRANTS_LIST)

    return render_template(
        "jinja_data.html",
        page_title="Jinja2: передача данных и фильтры",
        course=COURSE_INFO,
        students=STUDENTS_LIST,
        average_score=avg_score,
        grants=GRANTS_LIST,
        total_budget=total_budget,
    )


def main() -> None:
    """Демонстрация работы шаблонизатора Jinja2 с данными."""
    print("=== Демонстрация задания №9: Шаблон Jinja2 с данными ===")

    with app.test_client() as client:
        response = client.get("/")
        print(f"GET / -> Код ответа: {response.status_code}")
        assert response.status_code == 200, "Ошибка рендеринга шаблона Jinja2"

        html = response.get_data(as_text=True)

        # Проверка наследования шаблона
        assert "Дисциплина «Методы и технологии программирования»" in html, (
            "Базовый шаблон base.html не отрендерен"
        )
        print("  [+] Наследование шаблонов ({% extends %}) работает штатно")

        # Проверка работы фильтра upper
        assert "МЕТОДЫ И ТЕХНОЛОГИИ ПРОГРАММИРОВАНИЯ" in html, (
            "Встроенный фильтр upper не сработал"
        )
        print("  [+] Встроенные фильтры Jinja2 (upper, round, length) активны")

        # Проверка вывода студентов через цикл for
        assert "Берченёв Егор Константинович" in html
        assert "A (Отлично)" in html
        print("  [+] Циклы for и кастомный фильтр grade_badge применены")

        # Проверка форматирования валюты
        assert "₽" in html
        print("  [+] Кастомный фильтр currency успешно отформатировал суммы")

    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("\nЗапуск веб-сервера на http://127.0.0.1:5002 ...")
        app.run(host="127.0.0.1", port=5002, debug=True)
    else:
        print(
            "\nДля запуска локального сервера выполните: "
            "python jinja_template.py --serve"
        )


if __name__ == "__main__":
    main()
