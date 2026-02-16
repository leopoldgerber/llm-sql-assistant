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
