from __future__ import annotations

from pathlib import Path

from molbatch.backends.base import Backend
from molbatch.types import Plan
from molbatch.utils.chains import parse_chain_string
from molbatch.utils.platform import as_viewer_path


class PyMOLBackend(Backend):
    name = "pymol"
    script_suffix = ".pml"

    @staticmethod
    def _obj_ref(name: str) -> str:
        return f"%{name}"

    def _align_expr(self, plan: Plan, object_name: str, role: str) -> str:
        expr = f"({self._obj_ref(object_name)}) and chain {plan.config.alignment.chain}"
        if plan.config.alignment.use_atom_name:
            expr += f" and name {plan.config.alignment.atom_name}"
        extra = (
            plan.config.alignment.extra_mobile_selection
            if role == "mobile"
            else plan.config.alignment.extra_target_selection
        )
        if extra:
            expr += f" and ({extra})"
        return expr

    @staticmethod
    def _chain_expr(chains: list[str]) -> str:
        return "(" + " or ".join([f"chain {c}" for c in chains]) + ")"

    def render(self, plan: Plan) -> str:
        cfg = plan.config
        lines: list[str] = [
            "reinitialize",
            "set quiet, 1",
            f"bg_color {cfg.style.background_color}",
            f"set ray_trace_mode, {cfg.style.ray_trace_mode}",
            f'print "MolBatch backend: {self.name}"',
        ]
        lines.extend(cfg.hooks.pre_commands)

        for item in plan.structures:
            lines.append(f'load "{as_viewer_path(item.path)}", {item.object_name}')

        ref = plan.reference.object_name
        for item in plan.structures:
            if item.object_name == ref:
                continue
            mobile = self._align_expr(plan, item.object_name, "mobile")
            target = self._align_expr(plan, ref, "target")
            method = cfg.alignment.method
            if method == "align":
                lines.append(f"align {mobile}, {target}")
            elif method == "super":
                lines.append(f"super {mobile}, {target}")
            elif method == "cealign":
                lines.append(f"cealign {target}, {mobile}")
            else:
                lines.append(f'print "Skipping unsupported PyMOL alignment method: {method}"')

        def keep_only(obj_name: str, keep_chains: list[str]) -> None:
            expr = f"({self._obj_ref(obj_name)}) and not {self._chain_expr(keep_chains)}"
            if cfg.selection.keep_mode == "remove":
                lines.append(f"remove {expr}")
            else:
                lines.append(f"hide everything, {expr}")

        keep_only(ref, plan.reference_keep_chains)
        for item in plan.structures:
            if item.object_name != ref:
                keep_only(item.object_name, plan.display_chains)

        lines.append("hide everything, all")
        ref_core_chains = parse_chain_string(cfg.selection.reference_core_chains)
        ref_core = f"({self._obj_ref(ref)}) and {self._chain_expr(ref_core_chains)}"
        lines.append(f"show cartoon, {ref_core}")
        lines.append(f"color {cfg.style.reference_core_color}, {ref_core}")

        if cfg.style.show_reference_surface:
            lines.append(f"show surface, {ref_core}")
            lines.append(f"set transparency, {cfg.style.surface_transparency}, {ref_core}")

        if cfg.selection.show_reference_display_chains:
            ref_display_color = cfg.style.reference_display_color or cfg.style.reference_core_color
            for chain_id in plan.display_chains:
                base = f"({self._obj_ref(ref)}) and chain {chain_id}"
                lines.append(f"show sticks, {base}")
                lines.append(f"set stick_radius, {cfg.style.stick_radius}, {base}")
                lines.append(f"color {ref_display_color}, {base}")

        for item in plan.structures:
            if item.object_name == ref:
                continue
            color_name = plan.object_color_map[item.object_name]
            for chain_id in plan.display_chains:
                base = f"({self._obj_ref(item.object_name)}) and chain {chain_id}"
                polymer = f"({base}) and polymer"
                organic = f"({base}) and organic"
                other = f"({base}) and not polymer and not organic"
                lines.append(f"show cartoon, {polymer}")
                lines.append(f"show sticks, {organic}")
                lines.append(f"show sticks, {other}")
                lines.append(f"set stick_radius, {cfg.style.stick_radius}, {base}")
                lines.append(f"color {color_name}, {base}")
                if cfg.style.object_opacity is not None:
                    lines.append(f"set transparency, {cfg.style.object_opacity}, {base}")

        if cfg.selection.label_objects:
            for item in plan.structures:
                label_sel = f"({self._obj_ref(item.object_name)}) and name {cfg.alignment.atom_name}"
                lines.append(f'label first {label_sel}, "{item.object_name}"')

        lines.append(
            f"set cartoon_transparency, {cfg.style.cartoon_transparency_non_reference}, not ({ref_core})"
        )
        if cfg.style.center_on_reference:
            lines.append(f"center {ref_core}")
        if cfg.style.auto_orient:
            lines.append(f"orient {ref_core}")

        if cfg.output.save_session:
            session_path = Path(cfg.output.directory) / f"{cfg.output.basename}.pse"
            lines.append(f'save "{session_path.as_posix()}"')
        if cfg.output.save_image:
            image_path = Path(cfg.output.directory) / f"{cfg.output.basename}.png"
            lines.append(
                f'png "{image_path.as_posix()}", width={cfg.output.image_width}, height={cfg.output.image_height}, ray=1'
            )

        lines.extend(cfg.hooks.post_commands)
        lines.append('print "MolBatch completed."')
        return "\n".join(lines) + "\n"
