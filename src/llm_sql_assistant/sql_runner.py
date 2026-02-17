import sqlite3
from pathlib import Path
from dataclasses import dataclass

from llm_sql_assistant.sql_guardrails import is_sql_safe


@dataclass(frozen=True)
class SqlExecutionResult:
    rows: list[tuple]
    columns: list[str]


class SqlExecutionError(Exception):
    """Raised when SQL execution fails."""


def run_sql(db_path: Path, sql: str) -> SqlExecutionResult:
    """Execute a SQL query against a SQLite database.

    Args:
        db_path: Path to a SQLite database file.
        sql: SQL query string to execute.

    Returns:
        Query result with rows and column names.

    Raises:
        ValueError: If SQL is considered unsafe.
        FileNotFoundError: If the database file does not exist.
        SqlExecutionError: If execution fails for other reasons.
    """
    if not db_path.exists():
        raise FileNotFoundError(f'Database not found: {db_path}')

    if not is_sql_safe(sql):
        raise ValueError('SQL is not safe to execute.')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()
        columns = [
            d[0] for d in cursor.description
        ] if cursor.description else []
        return SqlExecutionResult(rows=rows, columns=columns)
    except sqlite3.Error as exc:
        raise SqlExecutionError(str(exc)) from exc
    finally:
        try:
            conn.close()
        except UnboundLocalError:
            pass
