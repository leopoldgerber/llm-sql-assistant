import re


_FORBIDDEN_KEYWORDS = (
    'delete',
    'update',
    'insert',
    'drop',
    'alter',
    'truncate',
    'create',
    'replace',
    'merge',
    'grant',
    'revoke',
)

_ALLOWED_START_KEYWORDS = ('select', 'with')


def is_sql_safe(sql: str) -> bool:
    """Check whether a SQL string is safe to execute.

    Rules (initial version):
    - Only SELECT queries are allowed.
    - WITH ... SELECT is allowed.
    - DDL/DML and privilege statements are rejected.

    Args:
        sql: A SQL query string.

    Returns:
        True if the query is considered safe, otherwise False.
    """
    normalized = _normalize_sql(sql)
    if not normalized:
        return False

    if not _starts_with_allowed_keyword(normalized):
        return False

    if _contains_forbidden_keyword(normalized):
        return False

    return True


def _normalize_sql(sql: str) -> str:
    """Normalize SQL for keyword checks."""
    sql = sql.strip().strip(';')
    sql = re.sub(r'\s+', ' ', sql)
    return sql.lower()


def _starts_with_allowed_keyword(normalized_sql: str) -> bool:
    return any(normalized_sql.startswith(k) for k in _ALLOWED_START_KEYWORDS)


def _contains_forbidden_keyword(normalized_sql: str) -> bool:
    # Word-boundary match to avoid false positives like "dropdown".
    for keyword in _FORBIDDEN_KEYWORDS:
        if re.search(rf'\b{re.escape(keyword)}\b', normalized_sql):
            return True
    return False
