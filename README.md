# Innowise Trainee Database Task

CLI-утилита на Python для загрузки данных о комнатах и студентах из JSON-файлов в PostgreSQL, выполнения аналитических SQL-запросов и экспорта результатов в формат JSON или XML.

## Стек технологий
- **Python 3.10+**
- **PostgreSQL**
- **psycopg2-binary**, **python-dotenv**

## Подготовка и запуск

### 1. Клонирование репозитория и установка зависимостей
```bash
git clone <url-репозитория>
cd <папка-проекта>
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
pip install -r requirements.txt