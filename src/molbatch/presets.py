from __future__ import annotations

from copy import deepcopy

from molbatch.types import AppConfig


PRESET_NAMES = ["comparison", "ligand-focus", "presentation", "minimal", "publication", "screening"]


def apply_preset(config: AppConfig) -> AppConfig:
    cfg = deepcopy(config)
    preset = cfg.style.preset

    if preset == "comparison":
        cfg.style.color_by_object = True
        cfg.output.save_session = True
    elif preset == "ligand-focus":
        cfg.style.stick_radius = max(cfg.style.stick_radius, 0.26)
        cfg.output.save_image = True
    elif preset == "presentation":
        cfg.style.cartoon_transparency_non_reference = 0.1
        cfg.output.save_session = True
        cfg.output.save_image = True
        cfg.output.image_supersample = max(cfg.output.image_supersample, 3)
        cfg.selection.label_objects = cfg.selection.label_objects or True
    elif preset == "minimal":
        cfg.output.save_session = False
        cfg.output.save_image = False
    elif preset == "publication":
        cfg.output.save_image = True
        cfg.output.save_session = True
        cfg.style.background_color = "white"
        cfg.style.show_reference_surface = False
        cfg.style.cartoon_transparency_non_reference = 0.05
        cfg.output.image_supersample = max(cfg.output.image_supersample, 4)
    elif preset == "screening":
        cfg.input.recursive = True
        cfg.output.report_markdown = True
        cfg.output.write_plan_json = True
        cfg.style.show_reference_surface = False
    else:
        raise ValueError(f"Unknown preset: {preset}")

    return cfg
