from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class ProjectConfig:
    name: str = "MolBatch"
    author: str = "PerinMu"


@dataclass
class InputConfig:
    directory: str = "."
    patterns: list[str] = field(default_factory=lambda: ["*.cif"])
    recursive: bool = False
    exclude_patterns: list[str] = field(default_factory=list)
    sort_by: str = "name"
    limit: int = 0


@dataclass
class ReferenceConfig:
    selector: str = "first"
    stem: str = ""
    regex: str = ""
    index: int = 0


@dataclass
class AlignmentConfig:
    method: str = "super"
    chain: str = "A"
    use_atom_name: bool = True
    atom_name: str = "CA"
    extra_mobile_selection: str = ""
    extra_target_selection: str = ""


@dataclass
class SelectionConfig:
    reference_core_chains: str = "ACE"
    display_chains: str = "XYZ"
    show_reference_display_chains: bool = True
    keep_mode: str = "hide_only"
    label_objects: bool = False


@dataclass
class StyleConfig:
    preset: str = "comparison"
    reference_core_color: str = "red"
    reference_display_color: str | None = "white"
    object_palette: list[str] = field(default_factory=lambda: [
        "cyan", "magenta", "yellow", "green", "orange", "tv_blue",
        "salmon", "lime", "slate", "violet", "marine", "olive",
        "pink", "teal", "wheat", "lightblue",
    ])
    stick_radius: float = 0.22
    cartoon_transparency_non_reference: float = 0.15
    object_opacity: float | None = None
    color_by_object: bool = True
    background_color: str = "white"
    ray_trace_mode: int = 1
    show_reference_surface: bool = False
    surface_transparency: float = 0.75
    center_on_reference: bool = True
    auto_orient: bool = True


@dataclass
class OutputConfig:
    directory: str = "out"
    basename: str = "scene"
    save_session: bool = False
    save_image: bool = False
    image_width: int = 1600
    image_height: int = 1200
    image_supersample: int = 3
    report_json: bool = True
    report_csv: bool = True
    report_markdown: bool = True
    write_plan_json: bool = True


@dataclass
class RuntimeConfig:
    auto_launch: bool = False
    headless: bool = False
    executable: str = ""
    args: list[str] = field(default_factory=list)
    shell: bool = False
    working_directory: str = ""


@dataclass
class HooksConfig:
    plugin_modules: list[str] = field(default_factory=list)
    pre_commands: list[str] = field(default_factory=list)
    post_commands: list[str] = field(default_factory=list)


@dataclass
class AppConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    input: InputConfig = field(default_factory=InputConfig)
    reference: ReferenceConfig = field(default_factory=ReferenceConfig)
    alignment: AlignmentConfig = field(default_factory=AlignmentConfig)
    selection: SelectionConfig = field(default_factory=SelectionConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    hooks: HooksConfig = field(default_factory=HooksConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StructureItem:
    path: Path
    stem: str
    object_name: str
    order_index: int


@dataclass
class Plan:
    config: AppConfig
    structures: list[StructureItem]
    reference: StructureItem
    display_chains: list[str]
    reference_keep_chains: list[str]
    object_color_map: dict[str, str]
    backend: str
    output_script: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.config.project.to_dict() if hasattr(self.config.project, "to_dict") else {
                "name": self.config.project.name,
                "author": self.config.project.author,
            },
            "backend": self.backend,
            "reference": {
                "stem": self.reference.stem,
                "object_name": self.reference.object_name,
                "path": str(self.reference.path),
            },
            "display_chains": self.display_chains,
            "reference_keep_chains": self.reference_keep_chains,
            "structures": [
                {
                    "order_index": item.order_index,
                    "path": str(item.path),
                    "stem": item.stem,
                    "object_name": item.object_name,
                    "is_reference": item.object_name == self.reference.object_name,
                    "object_color": self.object_color_map.get(item.object_name, ""),
                }
                for item in self.structures
            ],
        }
