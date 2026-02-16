from llm_sql_assistant.sql_guardrails import is_sql_safe


def test_is_sql_safe_rejects_dml() -> None:
    assert is_sql_safe('DELETE FROM users;') is False
