import psycopg2
from psycopg2.extras import RealDictCursor, execute_values


class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.close()

    def connect(self):
        """Connecting to a PostgreSQL database."""
        self.conn = psycopg2.connect(**self.db_config)

    def close(self):
        """Closing the connection."""
        if self.conn:
            self.conn.close()

    def execute_ddl(self, sql_query):
        """Executes DDL statements (e.g., CREATE TABLE)."""
        with self.conn.cursor() as cursor:
            cursor.execute(sql_query)
        self.conn.commit()

    def execute_batch(self, query, data):
        """Executes batch insert queries."""
        with self.conn.cursor() as cursor:
            execute_values(cursor, query, data)
        self.conn.commit()

    def fetch_all(self, sql_query):
        """Executes a SELECT query and returns rows as dictionaries."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_query)
            return cursor.fetchall()
        

class SchemaInitializer:
    """Responsible for creating database tables if they do not exist."""

    def __init__(self, db_manager: DatabaseManager, schema_path: str = "schema.sql"):
        self.db = db_manager
        self.schema_path = schema_path

    def init_schema(self):
        with open(self.schema_path, "r", encoding="utf-8") as f:
            ddl = f.read()
        self.db.execute_ddl(ddl)


class RoomRepository:
    """Handles database operations for the rooms table."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def bulk_insert(self, rooms):
        rooms_data = [(r["id"], r["name"]) for r in rooms]
        query = "INSERT INTO rooms (id, name) VALUES %s ON CONFLICT (id) DO NOTHING;"
        self.db.execute_batch(query, rooms_data)


class StudentRepository:
    """Handles database operations for the students table."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def bulk_insert(self, students):
        students_data = [
            (s["id"], s["name"], s["birthday"], s["sex"], s["room"])
            for s in students
        ]
        query = (
            "INSERT INTO students (id, name, birthday, sex, room) "
            "VALUES %s ON CONFLICT (id) DO NOTHING;"
        )
        self.db.execute_batch(query, students_data)
        