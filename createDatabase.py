# Changes from the old code:
#Environment variables for database credentials (config.env)
# terminates active connections before dropping (did this cause i was getting a lot of errors)
# used loop for table creation
# used directory for csv
# rror handling

import psycopg2
from dotenv import load_dotenv
import os

# Loading environment variables (config.env) for database connection
load_dotenv("config.env")

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "postgres"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "sql"),
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

# connecting to postgres and recreating target database 
conn = psycopg2.connect(
    dbname="postgres",
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"]
)
conn.autocommit = True
cur = conn.cursor()

# terminating active connections, recreating database 
cur.execute(f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '{DB_CONFIG["dbname"]}'
    AND pid <> pg_backend_pid();
""")
cur.execute(f'DROP DATABASE IF EXISTS "{DB_CONFIG["dbname"]}"')
cur.execute(f'CREATE DATABASE "{DB_CONFIG["dbname"]}"')

cur.close()
conn.close()

# connecting to the database we just made and making tables 
conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = True
cur = conn.cursor()

cur.execute('''
    CREATE TABLE "CUSTOMER" (
        "CUS_CODE" INT PRIMARY KEY,
        "CUS_LNAME" VARCHAR(20),
        "CUS_FNAME" VARCHAR(20),
        "CUS_INITIAL" CHAR(10),
        "CUS_AREACODE" VARCHAR(20),
        "CUS_PHONE" VARCHAR(20),
        "CUS_BALANCE" FLOAT
    );
    CREATE TABLE "INVOICE" (
        "INV_NUMBER" INT PRIMARY KEY,
        "CUS_CODE" INT,
        "INV_DATE" DATE
    );
    CREATE TABLE "LINE" (
        "LINE_NUMBER" INT,
        "INV_NUMBER" INT,
        "P_CODE" VARCHAR(20),
        "LINE_UNITS" FLOAT,
        "LINE_PRICE" FLOAT
    );
    CREATE TABLE "PRODUCT" (
        "P_CODE" VARCHAR(20) PRIMARY KEY,
        "P_DESCRIPT" VARCHAR(255),
        "P_INDATE" DATE,
        "P_QOH" INT,
        "P_MIN" INT,
        "P_PRICE" FLOAT,
        "P_DISCOUNT" FLOAT,
        "V_CODE" INT
    );
    CREATE TABLE "VENDOR" (
        "V_CODE" INT PRIMARY KEY,
        "V_NAME" VARCHAR(30),
        "V_AREACODE" VARCHAR(20),
        "V_CONTACT" VARCHAR(20),
        "V_PHONE" VARCHAR(20),
        "V_STATE" VARCHAR(20),
        "V_ORDER" VARCHAR(20)
    );
''')

# loading data from csv
base_dir = os.path.dirname(os.path.abspath(__file__))  # script for file path
csv_files = {
    "CUSTOMER": os.path.join(base_dir, "database", "CUSTOMER.csv"),
    "INVOICE": os.path.join(base_dir, "database", "INVOICE.csv"),
    "LINE": os.path.join(base_dir, "database", "LINE.csv"),
    "PRODUCT": os.path.join(base_dir, "database", "PRODUCT.csv"),
    "VENDOR": os.path.join(base_dir, "database", "VENDOR.csv")
}

for table, file_path in csv_files.items(): #using loops
    try:
        with open(file_path, 'r') as file:
            cur.copy_expert(f'COPY "{table}" FROM STDIN WITH CSV HEADER', file)
        print(f"Successfully loaded data into {table}.")
    except FileNotFoundError:
        print(f"CSV for {table} wasn't found, skipping this.")
    except Exception as e:
        print(f"Error loading data into {table}: {e}")

cur.close()
conn.close()
print("The Database setup has been completed.")
