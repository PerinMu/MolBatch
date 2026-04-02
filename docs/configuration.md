# Configuration

MolBatch supports YAML, JSON, and TOML configuration files.

## Main sections

- `project`: project metadata such as name and author
- `input`: discovery rules, include patterns, exclude patterns, sorting, and limits
- `reference`: reference selection by first item, index, exact stem, or regex
- `alignment`: method, chain, atom name, and extra selection filters
- `selection`: core chains, display chains, keep mode, and optional labeling
- `style`: colors, stick radius, transparency, background, surface display, and camera behavior
- `output`: output directory, basename, session/image export, and report formats
- `runtime`: optional viewer launch settings
- `hooks`: Python hook modules plus plain pre-commands and post-commands
