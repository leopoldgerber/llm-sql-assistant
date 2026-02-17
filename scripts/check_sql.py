import sys  # noqa
import argparse

from llm_sql_assistant.sql_guardrails import is_sql_safe


def main() -> int:
    """Run a command-line SQL safety check."""
    parser = argparse.ArgumentParser(
        description='Check whether SQL is safe to execute.')
    parser.add_argument('sql', help='SQL query string to check.')
    args = parser.parse_args()

    safe = is_sql_safe(args.sql)
    if safe:
        print('SAFE')
        return 0

    print('UNSAFE')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
