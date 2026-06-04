from __future__ import annotations

import argparse
import json
from pathlib import Path

from projectionbench.runner import BenchmarkRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="projectionbench",
        description="Run generic theory and ProjectionBench evaluations.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run an evaluation scenario")
    run.add_argument("scenario", help="Path to scenario JSON file")
    run.add_argument("--out", help="Optional path to write JSON-LD evaluation output")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        runner = BenchmarkRunner()
        result = runner.run_file(args.scenario)
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            Path(args.out).write_text(rendered + "\n", encoding="utf-8")
        print(rendered)


if __name__ == "__main__":
    main()
