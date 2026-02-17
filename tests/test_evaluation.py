import sqlite3
import pytest
from pathlib import Path

from llm_sql_assistant.evaluation import execution_match
from llm_sql_assistant.sql_runner import SqlExecutionError


def _create_test_db(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
    cursor.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?);",
        [(1, "Alice"), (2, "Bob"), (3, "Charlie")],
    )
    conn.commit()
    conn.close()


def test_execution_match_true(tmp_path: Path) -> None:
    db_path = tmp_path / "db.db"
    _create_test_db(db_path)

    predicted = "SELECT name FROM users WHERE id <= 2;"
    gold = "SELECT name FROM users WHERE id IN (1, 2);"

    assert (
        execution_match(
            db_path=db_path,
            predicted_sql=predicted,
            gold_sql=gold
        ) is True
    )


def test_execution_match_false(tmp_path: Path) -> None:
    db_path = tmp_path / "db.db"
    _create_test_db(db_path)

    predicted = "SELECT name FROM users WHERE id = 1;"
    gold = "SELECT name FROM users WHERE id IN (1, 2);"

    assert (
        execution_match(
            db_path=db_path,
            predicted_sql=predicted,
            gold_sql=gold
        )
        is False
    )


def test_execution_match_raises_on_invalid_sql(tmp_path: Path) -> None:
    db_path = tmp_path / "db.db"
    _create_test_db(db_path)

    predicted = "SELECT missing_column FROM users;"
    gold = "SELECT name FROM users;"

    with pytest.raises(SqlExecutionError):
        execution_match(
            db_path=db_path,
            predicted_sql=predicted,
            gold_sql=gold
        )
