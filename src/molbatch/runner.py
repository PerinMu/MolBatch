from __future__ import annotations

import logging
import shlex
import subprocess
from pathlib import Path

from molbatch.exceptions import RuntimeErrorExternal
from molbatch.types import AppConfig

logger = logging.getLogger(__name__)


def build_launch_command(config: AppConfig, backend: str, script_path: Path) -> list[str]:
    if config.runtime.executable:
        cmd = [config.runtime.executable, *config.runtime.args]
    else:
        if backend == "pymol":
            cmd = ["pymol", "-cq"] if config.runtime.headless else ["pymol"]
        elif backend == "chimerax":
            cmd = ["ChimeraX", "--nogui", "--exit", "--script"] if config.runtime.headless else ["ChimeraX", "--script"]
        else:
            raise RuntimeErrorExternal(f"Unsupported backend for runtime launch: {backend}")
    cmd.append(str(script_path))
    return cmd


def launch_script(config: AppConfig, backend: str, script_path: Path) -> int:
    command = build_launch_command(config, backend, script_path)
    logger.info("Launching external viewer: %s", shlex.join(command))
    try:
        completed = subprocess.run(command, check=False, shell=config.runtime.shell)
    except OSError as exc:
        raise RuntimeErrorExternal(str(exc)) from exc
    return completed.returncode
