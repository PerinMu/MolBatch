from __future__ import annotations

from pathlib import Path

from molbatch.backends.base import Backend
from molbatch.types import Plan
from molbatch.utils.platform import as_viewer_path


class ChimeraXBackend(Backend):
    name = "chimerax"
    script_suffix = ".cxc"

    def render(self, plan: Plan) -> str:
        cfg = plan.config
        lines: list[str] = [
            "close all",
            f"set bgColor {cfg.style.background_color}",
            f"# MolBatch backend: {self.name}",
        ]
        lines.extend(cfg.hooks.pre_commands)

        for item in plan.structures:
            lines.append(f'open "{as_viewer_path(item.path)}"')

        ref_model = f"#{plan.reference.order_index + 1}"
        for item in plan.structures:
            if item.object_name == plan.reference.object_name:
                continue
            mobile_model = f"#{item.order_index + 1}"
            if cfg.alignment.chain:
                lines.append(
                    f"mmaker {mobile_model}/{cfg.alignment.chain} to {ref_model}/{cfg.alignment.chain}"
                )
            else:
                lines.append(f"mmaker {mobile_model} to {ref_model}")

        lines.append("hide")
        for chain_id in plan.reference_keep_chains:
            lines.append(f"show {ref_model}/{chain_id}")
        lines.append(f"style {ref_model} cartoon")
        lines.append(f"color {cfg.style.reference_core_color} {ref_model}")

        if cfg.style.show_reference_surface:
            lines.append(f"surface {ref_model}")
            lines.append(f"transparency {int(cfg.style.surface_transparency * 100)} {ref_model}")

        if cfg.selection.show_reference_display_chains:
            ref_display_color = cfg.style.reference_display_color or cfg.style.reference_core_color
            for chain_id in plan.display_chains:
                lines.append(f"style {ref_model}/{chain_id} stick")
                lines.append(f"color {ref_display_color} {ref_model}/{chain_id}")

        for item in plan.structures:
            if item.object_name == plan.reference.object_name:
                continue
            model = f"#{item.order_index + 1}"
            color_name = plan.object_color_map[item.object_name]
            for chain_id in plan.display_chains:
                lines.append(f"show {model}/{chain_id}")
                lines.append(f"style {model}/{chain_id} stick")
                lines.append(f"color {color_name} {model}/{chain_id}")
                if cfg.style.object_opacity is not None:
                    lines.append(f"transparency {int(cfg.style.object_opacity * 100)} {model}/{chain_id}")

        if cfg.style.center_on_reference:
            lines.append(f"view {ref_model}")

        if cfg.output.save_session:
            session_path = Path(cfg.output.directory) / f"{cfg.output.basename}.cxs"
            lines.append(f'save "{session_path.as_posix()}"')
        if cfg.output.save_image:
            image_path = Path(cfg.output.directory) / f"{cfg.output.basename}.png"
            lines.append(
                f'save "{image_path.as_posix()}" width {cfg.output.image_width} height {cfg.output.image_height} supersample {cfg.output.image_supersample}'
            )

        lines.extend(cfg.hooks.post_commands)
        return "\n".join(lines) + "\n"
