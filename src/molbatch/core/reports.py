from __future__ import annotations

import csv
import json
from pathlib import Path

from molbatch.types import Plan


def _rows(plan: Plan) -> list[dict[str, object]]:
    rows = []
    for item in plan.structures:
        rows.append(
            {
                "order_index": item.order_index,
                "file": str(item.path),
                "stem": item.stem,
                "object_name": item.object_name,
                "is_reference": item.object_name == plan.reference.object_name,
                "object_color": plan.object_color_map.get(item.object_name, ""),
            }
        )
    return rows


def _write_markdown(plan: Plan, out_dir: Path, rows: list[dict[str, object]]) -> None:
    base = plan.config.output.basename
    lines = [
        f"# {plan.config.project.name} report",
        "",
        f"- Author: {plan.config.project.author}",
        f"- Backend: {plan.backend}",
        f"- Reference: `{plan.reference.stem}`",
        f"- Structures: {len(plan.structures)}",
        f"- Display chains: {', '.join(plan.display_chains)}",
        "",
        "## Structures",
        "",
        "| Index | Stem | Object name | Reference | Color | File |",
        "| ---: | --- | --- | :---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['order_index']} | {row['stem']} | {row['object_name']} | {'Yes' if row['is_reference'] else 'No'} | {row['object_color']} | `{row['file']}` |"
        )
    (out_dir / f"{base}_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reports(plan: Plan, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    base = plan.config.output.basename
    rows = _rows(plan)

    if plan.config.output.report_json:
        (out_dir / f"{base}_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    if plan.config.output.report_csv and rows:
        csv_path = out_dir / f"{base}_summary.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    if plan.config.output.report_markdown:
        _write_markdown(plan, out_dir, rows)

    if plan.config.output.write_plan_json:
        plan_json = {
            "config": plan.config.to_dict(),
            "plan": plan.to_dict(),
        }
        (out_dir / f"{base}_plan.json").write_text(json.dumps(plan_json, indent=2), encoding="utf-8")
