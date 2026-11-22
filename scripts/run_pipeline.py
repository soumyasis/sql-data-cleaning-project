import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
SQL_DIR = BASE_DIR / "sql"

DB_HOST = os.environ.get("MYSQL_HOST", "localhost")
DB_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
DB_NAME = "sales_cleaning"


def make_url(database=None):
    return URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=database,
    )


def get_engine():
    server_engine = create_engine(make_url())
    with server_engine.begin() as conn:
        conn.execute(text(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_bin"
        ))
    return create_engine(make_url(DB_NAME))


def ingest_csvs(engine):
    files = {
        "customers_master.csv": "stg_customers",
        "orders_raw.csv": "stg_orders",
    }
    for csv_name, table_name in files.items():
        df = pd.read_csv(RAW_DIR / csv_name, dtype=str, keep_default_na=False)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Ingested {len(df)} rows into {table_name}")


def main():
    engine = get_engine()
    ingest_csvs(engine)
    print("Ingestion complete.")


if __name__ == "__main__":
    main()