# llm-sql-assistant
LLM-based Text-to-SQL assistant with execution-accuracy evaluation and SQL safety guardrails.

---

## Goals
- Generate SQL `SELECT` queries from natural language user input.
- Ensure generated queries are safe and executable.
- Evaluate model quality using execution-based metrics.

---

## Roadmap
- Build baseline Text-to-SQL pipeline using a pretrained LLM.
- Add SQL guardrails (safety checks, restricted statements, validation).
- Implement execution-based evaluation.
- Introduce self-correction loop for failed queries.
- Fine-tune or specialize the model for improved SQL generation.
- Provide CLI or web-based demo.


## Quick SQL Guardrails Check (CLI)
You can quickly verify whether a SQL query is allowed by the guardrails using the built-in CLI tool.

Install the package in editable mode:

```bash
python -m pip install -e '.[dev]'
```

Run the checker:

```bash
python scripts/check_sql.py "SELECT * FROM users;"
python scripts/check_sql.py "DROP TABLE users;"
```

Expected behavior:

* Safe queries print `SAFE` and return exit code `0`
* Unsafe queries print `UNSAFE` and return exit code `1`

This small utility is helpful for debugging and demonstrating guardrail behavior directly from the terminal.


# Demo Database
Create a local SQLite database for testing:

```bash
python scripts/create_demo_db.py
```

This will generate a file called demo.db with sample customers and orders tables.