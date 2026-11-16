# Innowise Trainee Database Task

Консольная программа на Python для загрузки данных о комнатах и студентах из JSON-файлов в PostgreSQL, выполнения аналитических SQL-запросов и выгрузки отчетов в формат JSON или XML.

## Что использовано
- Python 3.10+
- PostgreSQL (запускается в Docker)
- Библиотеки: `psycopg2-binary`, `python-dotenv`

## Как запустить проект

### 1. Скачать проект и установить библиотеки
```bash
git clone <url-репозитория>
cd <папка-проекта>
python -m venv .venv
source .venv/bin/activate  # для Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настроить подключение к базе (.env)
Создайте файл `.env` на основе примера `.env.example` и впишите туда свои данные от базы:
```bash
cp .env.example .env
```

Внутри `.env` должно быть примерно так:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgre
DB_USER=admin
DB_PASSWORD=your_password
```

### 3. Поднять PostgreSQL в Docker
```bash
docker run --name students-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=postgre \
  -p 5432:5432 -d postgres
```

### 4. Запустить скрипт
Выгрузка результатов в JSON:
```bash
python main.py -s students.json -r rooms.json -f json
```

Выгрузка результатов в XML:
```bash
python main.py -s students.json -r rooms.json -f xml
```

**Флаги запуска:**
- `-s` (`--students`) — путь к файлу со студентами
- `-r` (`--rooms`) — путь к файлу с комнатами
- `-f` (`--format`) — формат отчетов (`json` или `xml`)

## Из каких файлов состоит проект
- `main.py` — главный файл: принимает флаги из консоли и запускает все этапы по очереди.
- `db.py` — подключение к PostgreSQL, создание таблиц/индексов и загрузка данных в базу.
- `queries.py` — 4 аналитических SQL-запроса.
- `exporters.py` — сохранение результатов в JSON и XML (через фабрику и базовый класс).
- `schema.sql` — SQL-скрипт создания таблиц `rooms` и `students`.
- `indexes.sql` — SQL-скрипт создания индексов (запускается после загрузки данных).
- `.env.example` — пример настроек подключения к БД.

## Какие индексы добавлены
В `indexes.sql` создаются два составных индекса для таблицы `students`:
- `idx_students_room_birthday` на `(room, birthday)` — помогает быстрее считать средний возраст и разницу возрастов по комнатам.
- `idx_students_room_sex` на `(room, sex)` — помогает быстрее находить комнаты, где живут студенты разного пола.