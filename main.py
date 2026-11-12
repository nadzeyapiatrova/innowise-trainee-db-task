import argparse
import json
from db import DatabaseManager
from queries import QUERIES
from exporters import ExporterFactory

# PostgreSQL connection parameters in Docker
DB_CONFIG = {
    "dbname": "postgre",
    "user": "admin",
    "password": "admin123",
    "host": "localhost",
    "port": "5432"
}


def load_json(filepath):
    """Function for reading a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # 1. Configuring command-line parameters (argparse)
    parser = argparse.ArgumentParser(description="Data import and analytics export.")
    parser.add_argument("-s", "--students", required=True, help="Path to the file containing students.")
    parser.add_argument("-r", "--rooms", required=True, help="Path to the file containing rooms.")
    parser.add_argument("-f", "--format", required=True, choices=["json", "xml"], help="Export format: json or xml")
    
    args = parser.parse_args()

    # 2. Reading files passed via the terminal
    print("1. Reading source files...")
    rooms_data = load_json(args.rooms)
    students_data = load_json(args.students)

    # 3. Connecting to the database and loading data
    db = DatabaseManager(DB_CONFIG)
    db.connect()

    try:
        print("2. Loading data into a database...")
        db.insert_rooms(rooms_data)
        db.insert_students(students_data)
        print("Data successfully saved to the database!")

        # 4. The required exporter (json or xml)
        exporter = ExporterFactory.get_exporter(args.format)

        # 5. Executing 4 analytical queries and save the results
        print(f"\n3. Executing queries and saving in .{args.format}:")
        for query_name, sql in QUERIES.items():
            rows = db.execute_query(sql)
            filename = f"{query_name}.{args.format}"
            exporter.export(rows, filename)

        print("\nAll 4 files have been successfully created!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
