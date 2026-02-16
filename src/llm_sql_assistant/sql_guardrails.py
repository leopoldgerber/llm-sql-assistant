def is_sql_safe(sql: str) -> bool:
    """Check whether a SQL string is safe to execute.

    The initial version is intentionally minimal. We'll improve it step-by-step.

    Args:
        sql: A SQL query string.

    Returns:
        True if the query is considered safe, otherwise False.
    """
    return True
