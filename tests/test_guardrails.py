from llm_sql_assistant.sql_guardrails import is_sql_safe


def test_is_sql_safe_rejects_dml() -> None:
    assert is_sql_safe('DELETE FROM users;') is False


def test_is_sql_safe_allows_select() -> None:
    assert is_sql_safe('SELECT * FROM users;') is True


def test_is_sql_safe_rejects_ddl() -> None:
    assert is_sql_safe('DROP TABLE users;') is False
