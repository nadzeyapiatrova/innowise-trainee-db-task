import argparse
import json
import os
from dotenv import load_dotenv  # pip install python-dotenv

from db import DatabaseManager, SchemaInitializer, RoomRepository, StudentRepository
from queries import QUERIES
from exporters import ExporterFactory, BaseExporter

load_dotenv()

class JsonLoader:
    """Responsible for reading and parsing JSON files."""

    def load(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


class AnalyticsPipeline:
    """Orchestrates data loading, database persistence, and report exporting."""

    def __init__(
        self,
        db_manager: DatabaseManager,
        schema_initializer: SchemaInitializer,
        room_repo: RoomRepository,
        student_repo: StudentRepository,
        loader: JsonLoader,
        exporter: BaseExporter,
        queries: dict,
    ):
        self.db = db_manager
        self.schema = schema_initializer
        self.room_repo = room_repo
        self.student_repo = student_repo
        self.loader = loader
        self.exporter = exporter
        self.queries = queries

    def run(self, rooms_path: str, students_path: str, output_format: str):
        print("1. Reading source files...")
        rooms_data = self.loader.load(rooms_path)
        students_data = self.loader.load(students_path)

        print("2. Preparing database and loading data...")
        self.schema.init_schema()
        self.room_repo.bulk_insert(rooms_data)
        self.student_repo.bulk_insert(students_data)
        self.schema.init_indexes()
        print("Data successfully saved to the database!")

        print(f"\n3. Executing queries and saving in .{output_format}:")
        for query_name, sql in self.queries.items():
            rows = self.db.fetch_all(sql)
            filename = f"{query_name}.{output_format}"
            self.exporter.export(rows, filename)

        print("\nAll files have been successfully created!")


def get_db_config():
    return {
        "dbname": os.getenv("DB_NAME", "postgre"),
        "user": os.getenv("DB_USER", "admin"),
        "password": os.getenv("DB_PASSWORD", "admin123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Data import and analytics export.")
    parser.add_argument("-s", "--students", required=True, help="Path to the file containing students.")
    parser.add_argument("-r", "--rooms", required=True, help="Path to the file containing rooms.")
    parser.add_argument("-f", "--format", required=True, choices=["json", "xml"], help="Export format: json or xml")
    return parser.parse_args()


def main():
    args = parse_args()
    db_config = get_db_config()

    with DatabaseManager(db_config) as db_manager:
        pipeline = AnalyticsPipeline(
            db_manager=db_manager,
            schema_initializer=SchemaInitializer(db_manager),
            room_repo=RoomRepository(db_manager),
            student_repo=StudentRepository(db_manager),
            loader=JsonLoader(),
            exporter=ExporterFactory.get_exporter(args.format),
            queries=QUERIES,
        )
        pipeline.run(
            rooms_path=args.rooms,
            students_path=args.students,
            output_format=args.format,
        )


if __name__ == "__main__":
    main()
