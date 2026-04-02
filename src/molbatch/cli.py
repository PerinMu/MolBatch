from __future__ import annotations

import argparse
import json
from pathlib import Path

from molbatch.backends import get_backend
from molbatch.backends.registry import available_backends
from molbatch.config import dump_config, load_config
from molbatch.core.planner import build_plan, discover_structure_items
from molbatch.core.reports import write_reports
from molbatch.logging_utils import configure_logging
from molbatch.plugins.hooks import HookManager
from molbatch.presets import PRESET_NAMES
from molbatch.runner import launch_script
from molbatch.types import AppConfig
from molbatch.utils.system import runtime_report


def _base_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="molbatch", description="Batch structure processing for PyMOL and ChimeraX")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-config", help="Write a starter config")
    init_parser.add_argument("--format", choices=["yaml", "json", "toml"], default="yaml")
    init_parser.add_argument("--out", type=Path, required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a config file")
    validate_parser.add_argument("--config", type=Path, required=True)

    scan_parser = subparsers.add_parser("scan", help="List matching structure files")
    scan_parser.add_argument("--config", type=Path, required=True)

    plan_parser = subparsers.add_parser("plan", help="Build and print a normalized execution plan")
    plan_parser.add_argument("--config", type=Path, required=True)
    plan_parser.add_argument("--backend", choices=available_backends(), default="pymol")

    subparsers.add_parser("list-presets", help="List built-in presets")
    subparsers.add_parser("list-backends", help="List supported backends")
    subparsers.add_parser("doctor", help="Print local runtime diagnostics")

    for name in ["generate", "run"]:
        command_parser = subparsers.add_parser(name, help=f"{name.capitalize()} a backend script")
        command_parser.add_argument("--config", type=Path, required=True)
        command_parser.add_argument("--backend", choices=available_backends(), required=True)
        command_parser.add_argument("--out", type=Path, default=None)
        command_parser.add_argument("--log-file", type=Path, default=None)

    return parser


def _write_default_config(path: Path, fmt: str) -> None:
    config = AppConfig()
    text = dump_config(config, fmt)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _generate_or_run(args: argparse.Namespace, do_run: bool) -> int:
    config = load_config(args.config)
    configure_logging(log_file=str(args.log_file) if args.log_file else None)
    backend = get_backend(args.backend)
    plan = build_plan(config, args.backend)
    hook_manager = HookManager(plan.config.hooks.plugin_modules)
    plan = hook_manager.before_render(plan)
    script_text = backend.render(plan)
    script_text = hook_manager.after_render(plan, script_text)

    out_path = args.out or backend.default_output_path(plan)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(script_text, encoding="utf-8")

    report_dir = Path(plan.config.output.directory)
    write_reports(plan, report_dir)

    if do_run or plan.config.runtime.auto_launch:
        return_code = launch_script(plan.config, args.backend, out_path)
        return return_code
    return 0


def main() -> int:
    parser = _base_parser()
    args = parser.parse_args()

    if args.command == "init-config":
        _write_default_config(args.out, args.format)
        return 0
    if args.command == "validate":
        config = load_config(args.config)
        print(json.dumps(config.to_dict(), indent=2))
        return 0
    if args.command == "scan":
        config = load_config(args.config)
        items = discover_structure_items(config)
        print(json.dumps([{"path": str(item.path), "stem": item.stem, "object_name": item.object_name} for item in items], indent=2))
        return 0
    if args.command == "plan":
        config = load_config(args.config)
        plan = build_plan(config, args.backend)
        print(json.dumps(plan.to_dict(), indent=2))
        return 0
    if args.command == "list-presets":
        for name in PRESET_NAMES:
            print(name)
        return 0
    if args.command == "list-backends":
        for name in available_backends():
            print(name)
        return 0
    if args.command == "doctor":
        print(json.dumps(runtime_report(), indent=2))
        return 0
    if args.command == "generate":
        return _generate_or_run(args, do_run=False)
    if args.command == "run":
        return _generate_or_run(args, do_run=True)

    parser.error(f"Unknown command: {args.command}")
    return 2
