"""
Database Engine & Connection Management
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

import os
import sqlite3
from typing import Dict, Any, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

def get_db_path() -> str:
    path = settings.DATABASE_PATH
    if not os.path.isabs(path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, path)
    return path

def get_sqlite_uri() -> str:
    db_path = get_db_path()
    return f"sqlite:///{db_path}"

engine = create_engine(
    get_sqlite_uri(),
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def execute_read_only_query(sql_query: str, max_rows: int = 50) -> Dict[str, Any]:
    """
    Executes a validated SELECT query on SQLite in read-only mode.
    Primary execution path uses SQLite URI mode 'file:{db_path}?mode=ro'.
    If URI mode fails with OperationalError, falls back to standard connection.
    Returns columns, rows, row_count, and execution metadata.
    """
    db_path = get_db_path()
    if not os.path.exists(db_path):
        from data.seed import init_db
        init_db(db_path)

    conn_uri = f"file:{db_path}?mode=ro"
    try:
        conn = sqlite3.connect(conn_uri, uri=True)
    except sqlite3.OperationalError:
        conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

        # Enforce max row limit safely
        if len(rows) > max_rows:
            rows = rows[:max_rows]

        processed_rows = []
        for row in rows:
            processed_row = []
            for val in row:
                if isinstance(val, (int, float, str, type(None))):
                    processed_row.append(val)
                else:
                    processed_row.append(str(val))
            processed_rows.append(processed_row)

        return {
            "columns": columns,
            "rows": processed_rows,
            "row_count": len(processed_rows),
            "success": True,
            "error": None
        }
    finally:
        conn.close()
