from __future__ import annotations

import re

from molbatch.core.colors import build_object_color_map
from molbatch.exceptions import PlanError
from molbatch.presets import apply_preset
from molbatch.types import AppConfig, Plan, StructureItem
from molbatch.utils.chains import merge_unique_chain_strings, parse_chain_string
from molbatch.utils.files import discover_files
from molbatch.utils.names import make_unique_object_name


def _resolve_reference(config: AppConfig, structures: list[StructureItem]) -> StructureItem:
    selector = config.reference.selector
    if selector == "first":
        return structures[0]
    if selector == "index":
        try:
            return structures[config.reference.index]
        except IndexError as exc:
            raise PlanError("reference.index is out of range") from exc
    if selector == "stem":
        for item in structures:
            if item.stem == config.reference.stem:
                return item
        raise PlanError(f"Reference stem not found: {config.reference.stem}")
    if selector == "regex":
        pattern = re.compile(config.reference.regex)
        for item in structures:
            if pattern.search(item.stem):
                return item
        raise PlanError(f"Reference regex did not match: {config.reference.regex}")
    raise PlanError(f"Unsupported reference selector: {selector}")


def discover_structure_items(config: AppConfig) -> list[StructureItem]:
    files = discover_files(
        config.input.directory,
        config.input.patterns,
        config.input.recursive,
        exclude_patterns=config.input.exclude_patterns,
        sort_by=config.input.sort_by,
        limit=config.input.limit,
    )
    used_names: set[str] = set()
    structures: list[StructureItem] = []
    for idx, path in enumerate(files):
        structures.append(
            StructureItem(
                path=path,
                stem=path.stem,
                object_name=make_unique_object_name(path.stem, used_names),
                order_index=idx,
            )
        )
    return structures


def build_plan(config: AppConfig, backend: str) -> Plan:
    cfg = apply_preset(config)
    structures = discover_structure_items(cfg)
    if not structures:
        raise PlanError(f"No structure files found in {cfg.input.directory}")

    reference = _resolve_reference(cfg, structures)
    display_chains = parse_chain_string(cfg.selection.display_chains)
    reference_keep = merge_unique_chain_strings(
        cfg.selection.reference_core_chains,
        cfg.selection.display_chains if cfg.selection.show_reference_display_chains else "",
    )
    object_color_map = build_object_color_map(
        [item.object_name for item in structures],
        reference.object_name,
        cfg.style.object_palette,
    )

    return Plan(
        config=cfg,
        structures=structures,
        reference=reference,
        display_chains=display_chains,
        reference_keep_chains=reference_keep,
        object_color_map=object_color_map,
        backend=backend,
    )
