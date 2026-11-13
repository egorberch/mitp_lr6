## Берченёв Егор Константинович, группа 220042-11, вариант 3, лабораторная №6

## "Веб-программирование на Python"

## Задания варианта 3:

### Средней сложности:
- №3 - Статическая страница + CSS (`static_page.py`)
- №5 - Страница с Bootstrap (`bootstrap_page.py`)
- №9 - Шаблон Jinja2 с данными (`jinja_template.py`)

### Повышенной сложности:
- №3 - Авторизация пользователя (`user_auth.py`)
- №7 - Деплой на Heroku (`heroku_deploy.py`)

## Описание структуры проекта:
- `static_page.py` — Flask-приложение для отдачи статического HTML и внешнего файла стилей CSS (Задание №3 средней сложности).
- `bootstrap_page.py` — адаптивный веб-интерфейс на фреймворке Bootstrap 5 с сеткой, карточками, интерактивной таблицей и модальным окном (Задание №5 средней сложности).
- `jinja_template.py` — демонстрация работы шаблонизатора Jinja2 с наследованием шаблонов, циклами, условиями, встроенными и кастомными фильтрами (Задание №9 средней сложности).
- `user_auth.py` — система регистрации и аутентификации пользователей с криптографическим хэшированием паролей, сессиями и защищённым личным кабинетом (Задание №3 повышенной сложности).
- `heroku_deploy.py` — облачное веб-приложение, оптимизированное для развертывания на Heroku по методологии 12-Factor App с healthcheck-эндпоинтом (Задание №7 повышенной сложности).
- `Procfile` — конфигурационный файл запуска веб-процесса Heroku с WSGI-сервером Gunicorn.
- `runtime.txt` — указание версии интерпретатора Python для среды Heroku.
- `templates/` — директория шаблонов Jinja2 (`base.html`, `static_page.html`, `bootstrap_page.html`, `jinja_data.html`, `login.html`, `register.html`, `dashboard.html`).
- `static/css/` — директория статических файлов стилей (`style.css`, `auth.css`).

## Инструкция по запуску:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Демонстрационный запуск и автоматическое тестирование модулей:
python static_page.py
python bootstrap_page.py
python jinja_template.py
python user_auth.py
python heroku_deploy.py

# Для интерактивного запуска локального веб-сервера добавьте флаг --serve:
# python static_page.py --serve      # Доступен на http://127.0.0.1:5000
# python bootstrap_page.py --serve   # Доступен на http://127.0.0.1:5001
# python jinja_template.py --serve   # Доступен на http://127.0.0.1:5002
# python user_auth.py --serve        # Доступен на http://127.0.0.1:5003
# python heroku_deploy.py --serve    # Доступен на http://127.0.0.1:5000
```

## Инструкция по деплою на Heroku:
```bash
# 1. Авторизация в Heroku CLI
heroku login

# 2. Создание нового облачного приложения
heroku create mitp-lr6-berchenev

# 3. Развертывание репозитория
git push heroku main

# 4. Открытие приложения в браузере
heroku open

# 5. Мониторинг логов контейнера
heroku logs --tail
```

Все скрипты оформлены по PEP8 и проверены FLAKE8 ( python -m flake8 . ).
