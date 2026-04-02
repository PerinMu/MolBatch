from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from molbatch.exceptions import ConfigError
from molbatch.types import (
    AlignmentConfig,
    AppConfig,
    HooksConfig,
    InputConfig,
    OutputConfig,
    ProjectConfig,
    ReferenceConfig,
    RuntimeConfig,
    SelectionConfig,
    StyleConfig,
)

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import yaml


def _read_mapping(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    if suffix == ".json":
        return json.loads(text)
    if suffix == ".toml":
        return tomllib.loads(text)
    raise ConfigError(f"Unsupported config format: {path.suffix}")


def _section(mapping: dict[str, Any], key: str) -> dict[str, Any]:
    value = mapping.get(key, {})
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError(f"Section '{key}' must be a mapping")
    return value


def load_config(path: str | Path) -> AppConfig:
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigError(f"Config not found: {cfg_path}")

    raw = _read_mapping(cfg_path)
    if not isinstance(raw, dict):
        raise ConfigError("Top-level config must be a mapping")

    config = AppConfig(
        project=ProjectConfig(**_section(raw, "project")),
        input=InputConfig(**_section(raw, "input")),
        reference=ReferenceConfig(**_section(raw, "reference")),
        alignment=AlignmentConfig(**_section(raw, "alignment")),
        selection=SelectionConfig(**_section(raw, "selection")),
        style=StyleConfig(**_section(raw, "style")),
        output=OutputConfig(**_section(raw, "output")),
        runtime=RuntimeConfig(**_section(raw, "runtime")),
        hooks=HooksConfig(**_section(raw, "hooks")),
    )

    validate_config(config)
    return config


def validate_config(config: AppConfig) -> None:
    if config.reference.selector not in {"first", "stem", "regex", "index"}:
        raise ConfigError("reference.selector must be one of: first, stem, regex, index")
    if config.reference.selector == "stem" and not config.reference.stem:
        raise ConfigError("reference.stem is required when selector='stem'")
    if config.reference.selector == "regex" and not config.reference.regex:
        raise ConfigError("reference.regex is required when selector='regex'")
    if config.selection.keep_mode not in {"hide_only", "remove"}:
        raise ConfigError("selection.keep_mode must be 'hide_only' or 'remove'")
    if config.alignment.method not in {"align", "super", "cealign", "matchmaker"}:
        raise ConfigError("Unsupported alignment method")
    if not config.input.patterns:
        raise ConfigError("At least one input pattern is required")
    if config.input.sort_by not in {"name", "stem", "path", "mtime"}:
        raise ConfigError("input.sort_by must be one of: name, stem, path, mtime")
    if config.input.limit < 0:
        raise ConfigError("input.limit must be >= 0")
    if config.output.image_width <= 0 or config.output.image_height <= 0:
        raise ConfigError("Image width and height must be positive")
    if config.style.stick_radius <= 0:
        raise ConfigError("style.stick_radius must be positive")
    if not (0 <= config.style.surface_transparency <= 1):
        raise ConfigError("style.surface_transparency must be between 0 and 1")


def dump_config(config: AppConfig, fmt: str) -> str:
    data = config.to_dict()
    fmt = fmt.lower()
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt in {"yaml", "yml"}:
        return yaml.safe_dump(data, sort_keys=False)
    if fmt == "toml":
        try:
            import tomli_w
        except ModuleNotFoundError as exc:
            raise ConfigError("tomli-w is required to write TOML configs") from exc
        return tomli_w.dumps(data)
    raise ConfigError(f"Unsupported output format: {fmt}")
