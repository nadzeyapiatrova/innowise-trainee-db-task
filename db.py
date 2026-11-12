import psycopg2
from psycopg2.extras import RealDictCursor, execute_values


class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    def connect(self):
        """Connecting to a PostgreSQL database."""
        self.conn = psycopg2.connect(**self.db_config)

    def close(self):
        """Closing the connection."""
        if self.conn:
            self.conn.close()

    def insert_rooms(self, rooms):
        """Loading rooms into the table rooms."""
        rooms_data = [(r["id"], r["name"]) for r in rooms]
        query = "INSERT INTO rooms (id, name) VALUES %s ON CONFLICT (id) DO NOTHING;"
        with self.conn.cursor() as cursor:
            execute_values(cursor, query, rooms_data)
        self.conn.commit()

    def insert_students(self, students):
        """Loading students into the table students."""
        students_data = [
            (s["id"], s["name"], s["birthday"], s["sex"], s["room"])
            for s in students
        ]
        query = (
            "INSERT INTO students (id, name, birthday, sex, room) "
            "VALUES %s ON CONFLICT (id) DO NOTHING;"
        )
        with self.conn.cursor() as cursor:
            execute_values(cursor, query, students_data)
        self.conn.commit()

    def execute_query(self, sql_query):
        """Executes an SQL query and returns rows as dictionaries."""
        # RealDictCursor is needed so that the result isn't just (1, 'Room 1'),
        # but includes the column names: {'id': 1, 'name': 'Room 1'}
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_query)
            return cursor.fetchall()
        