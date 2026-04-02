# Architecture

MolBatch is organized into five layers:

1. `config`: file loading and validation
2. `core`: file scanning, planning, and report generation
3. `backends`: PyMOL and ChimeraX script renderers
4. `runner`: optional external execution
5. `plugins`: hook-based extensibility

The planner remains backend-agnostic. Each backend receives the same normalized `Plan` object.
