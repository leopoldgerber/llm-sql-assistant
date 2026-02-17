import pytest
from pathlib import Path

from llm_sql_assistant.sql_runner import SqlExecutionError, run_sql


def test_run_sql_returns_rows(tmp_path: Path) -> None:
    db_path = tmp_path / 'demo.db'

    # Create a tiny temp DB for the test.
    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);')
    cursor.executemany(
        'INSERT INTO users (id, name) VALUES (?, ?);',
        [(1, 'Alice'), (2, 'Bob')],
    )
    conn.commit()
    conn.close()

    result = run_sql(
        db_path=db_path,
        sql='SELECT id, name FROM users ORDER BY id;'
    )

    assert result.columns == ['id', 'name']
    assert result.rows == [(1, 'Alice'), (2, 'Bob')]


def test_run_sql_rejects_unsafe_sql(tmp_path: Path) -> None:
    db_path = tmp_path / 'demo.db'
    db_path.write_bytes(b'')

    with pytest.raises(ValueError):
        run_sql(db_path=db_path, sql='DROP TABLE users;')


def test_run_sql_raises_execution_error(tmp_path: Path) -> None:
    db_path = tmp_path / 'demo.db'

    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);')
    conn.commit()
    conn.close()

    with pytest.raises(SqlExecutionError):
        run_sql(db_path=db_path, sql='SELECT missing_column FROM users;')
