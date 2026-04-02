# MolBatch

MolBatch is a full-featured batch structure processing toolkit for PyMOL and ChimeraX.
It converts one-off visualization scripts into a reusable, configurable, and extensible Python package for structural biology workflows.

## Maintainer

- PerinMu

## Highlights

- Batch discovery of `.cif`, `.mmcif`, and `.pdb` files
- Dual backends:
  - PyMOL script generation (`.pml`)
  - ChimeraX command generation (`.cxc`)
- Configuration via YAML, JSON, or TOML
- CLI subcommands for config initialization, validation, scanning, plan inspection, script generation, execution, preset listing, backend listing, and environment diagnostics
- Reference-based alignment planning
- Chain filtering, hiding, removing, and object-specific coloring
- Background color, reference surface, transparency, and image/session export controls
- Optional object labeling for presentation-style scenes
- Plugin-style Python hook support with pre-command and post-command injection
- Markdown, JSON, CSV, and normalized plan reports
- Cross-platform path handling for Windows, macOS, and Linux
- Project-ready repository layout with docs, tests, examples, and packaging files

## Installation

```bash
pip install -e .
```

For development:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
pytest
```

## Quick start

Create a starter configuration:

```bash
molbatch init-config --format yaml --out examples/demo.yaml
```

Validate the configuration:

```bash
molbatch validate --config examples/demo.yaml
```

Scan matching inputs:

```bash
molbatch scan --config examples/demo.yaml
```

Inspect a normalized execution plan:

```bash
molbatch plan --config examples/demo.yaml --backend pymol
```

Generate a PyMOL script:

```bash
molbatch generate --config examples/demo.yaml --backend pymol --out out/scene.pml
```

Generate a ChimeraX script:

```bash
molbatch generate --config examples/demo.yaml --backend chimerax --out out/scene.cxc
```

Run with a local installation:

```bash
molbatch run --config examples/demo.yaml --backend pymol --out out/scene.pml
```

Check local viewer availability:

```bash
molbatch doctor
```

## Project layout

```text
molbatch/
├─ docs/
├─ examples/
├─ src/molbatch/
│  ├─ backends/
│  ├─ core/
│  ├─ plugins/
│  └─ utils/
└─ tests/
```

## Core concepts

1. **Config loading** normalizes YAML/JSON/TOML into a shared internal model.
2. **Scanning** discovers files with include patterns, exclude patterns, sorting, and optional limits.
3. **Planning** resolves a reference structure, applies presets, and assigns colors.
4. **Backend rendering** turns the plan into a PyMOL or ChimeraX script.
5. **Runtime execution** can optionally launch an external viewer using configurable command templates.
6. **Hooks** let users inject custom Python logic and plain backend commands before or after script generation.

## Presets

Available built-in presets:

- `comparison`
- `ligand-focus`
- `presentation`
- `minimal`
- `publication`
- `screening`

List them from the CLI:

```bash
molbatch list-presets
```

## Example use cases

- Align many predicted structures to a reference chain
- Keep only selected core chains in the reference while showing ligand chains in every model
- Generate reproducible sessions and figures for manuscripts or slides
- Batch-prepare viewer scripts without editing commands manually
- Pre-scan large directories and archive reports for screening workflows

## License

Apache-2.0. See `LICENSE`.
