import json
from dataclasses import dataclass
from pathlib import Path

from llm_sql_assistant.evaluation import execution_match
from llm_sql_assistant.sql_runner import SqlExecutionError


@dataclass(frozen=True)
class EvalItemResult:
    example_id: str
    is_correct: bool
    error: str | None


def load_examples(path: Path) -> list[dict]:
    """Load evaluation examples from a JSONL file."""
    examples = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        examples.append(json.loads(line))
    return examples


def main() -> None:
    db_path = Path('demo.db')
    examples_path = Path('data/eval_examples.jsonl')

    if not db_path.exists():
        raise FileNotFoundError(
            'demo.db not found. Run: python scripts/create_demo_db.py'
        )

    examples = load_examples(examples_path)
    results: list[EvalItemResult] = []

    for ex in examples:
        example_id = ex['id']
        predicted_sql = ex['predicted_sql']
        gold_sql = ex['gold_sql']

        try:
            ok = execution_match(
                db_path=db_path,
                predicted_sql=predicted_sql,
                gold_sql=gold_sql,
            )
            results.append(
                EvalItemResult(
                    example_id=example_id,
                    is_correct=ok,
                    error=None
                )
            )
        except SqlExecutionError as exc:
            results.append(
                EvalItemResult(
                    example_id=example_id,
                    is_correct=False,
                    error=str(exc)
                )
            )

    total = len(results)
    correct = sum(1 for r in results if r.is_correct)
    accuracy = correct / total if total else 0.0

    print(f'Total: {total}')
    print(f'Correct: {correct}')
    print(f'Execution accuracy: {accuracy:.3f}')
    print('---')
    for r in results:
        if r.is_correct:
            status = 'OK'
        elif r.error:
            status = f'ERROR ({r.error})'
        else:
            status = 'WRONG'
        print(f'{r.example_id}: {status}')


if __name__ == '__main__':
    main()
