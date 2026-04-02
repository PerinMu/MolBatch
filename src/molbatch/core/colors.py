from __future__ import annotations


def build_object_color_map(object_names: list[str], reference_name: str, palette: list[str]) -> dict[str, str]:
    if not palette:
        palette = ["cyan"]
    mapping: dict[str, str] = {}
    color_idx = 0
    for name in object_names:
        if name == reference_name:
            continue
        mapping[name] = palette[color_idx % len(palette)]
        color_idx += 1
    return mapping
