import os
import time
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from .config import settings
load_dotenv()
# need the try statement
# we should only have the server running only if we cna connect to the database
while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="Local Postgres",
            user="postgres",
            password=settings.db_password,
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        # after an error we want for the reconnection to wait for 2 to 3 secs
        time.sleep(2)
