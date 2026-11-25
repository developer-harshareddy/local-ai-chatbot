
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from .env")

try:
    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("SELECT version();")

            database_version = cursor.fetchone()

            print("PostgreSQL connection successful!")

            print("Database version:")
            print(database_version[0])

except psycopg.Error as error:

    print("Database connection failed!")

    print(error)