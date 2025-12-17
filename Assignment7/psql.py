#!/usr/bin/env python3
import os
import sys
import psycopg
from psycopg.rows import dict_row


def get_conn_str() -> str:
    """
    Prefer a single DATABASE_URL, otherwise build from parts.
    Examples:
      export DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    dbname = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "demo123")

    # psycopg accepts keyword params too, but a conninfo string keeps it simple.
    return f"host={host} port={port} dbname={dbname} user={user} password={password}"


def create_table(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id   INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age  INTEGER NOT NULL CHECK (age >= 0)
            );
            """
        )
    conn.commit()


def insert_employees(conn: psycopg.Connection, rows: list[tuple[int, str, int]]) -> None:
    """
    Inserts rows like: (id, name, age)
    Uses UPSERT so re-running the script won't error if IDs already exist.
    """
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO employees (id, name, age)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name,
                age  = EXCLUDED.age;
            """,
            rows,
        )
    conn.commit()


def fetch_employees(conn: psycopg.Connection) -> list[dict]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT id, name, age FROM employees ORDER BY id;")
        return cur.fetchall()


def main() -> int:
    conninfo = get_conn_str()

    try:
        with psycopg.connect(conninfo) as conn:
            create_table(conn)

            sample_rows = [
                (1, "Alice", 30),
                (2, "Bob", 25),
                (3, "Charlie", 40),
            ]
            insert_employees(conn, sample_rows)

            data = fetch_employees(conn)
            print("Employees:")
            for row in data:
                print(f"  id={row['id']}, name={row['name']}, age={row['age']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
