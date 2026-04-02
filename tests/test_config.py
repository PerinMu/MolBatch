from pathlib import Path

from molbatch.config import load_config


def test_load_yaml_config(tmp_path: Path):
    path = tmp_path / "demo.yaml"
    path.write_text(
        """
project:
  name: Demo
input:
  directory: .
reference:
  selector: first
alignment:
  method: super
selection:
  keep_mode: hide_only
style:
  stick_radius: 0.22
output:
  image_width: 100
  image_height: 100
""",
        encoding="utf-8",
    )
    cfg = load_config(path)
    assert cfg.project.name == "Demo"
