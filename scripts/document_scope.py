"""Select maintained documents while preserving explicitly archived sources."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

try:
    from .config_utils import load_project_config
except ImportError:
    from config_utils import load_project_config


def archived_document_paths(config: dict[str, Any], root: Path) -> list[Path]:
    documentation = config.get("documentation", {})
    if not isinstance(documentation, dict):
        raise ValueError("documentation must be a mapping")
    entries = documentation.get("archived_paths", [])
    if not isinstance(entries, list):
        raise ValueError("documentation.archived_paths must be a list")
    paths = []
    for entry in entries:
        if not isinstance(entry, str) or not entry.strip():
            raise ValueError("documentation.archived_paths entries must be non-empty paths")
        path = Path(entry)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError(
                "documentation.archived_paths entries must be repository-relative paths "
                "without '..' and must not select the repository root"
            )
        if any(char in entry for char in "*?[]"):
            raise ValueError("documentation.archived_paths entries must be paths, not globs")
        paths.append(root / path)
    return paths


def maintained_documents(root: Path, extensions: set[str]) -> list[Path]:
    config_path = root / "project.yml"
    config = load_project_config(config_path) if config_path.is_file() else {}
    archives = archived_document_paths(config, root)
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
    )
    paths = {root / name for name in output.decode().split("\0") if name}
    return sorted(
        path
        for path in paths
        if path.suffix in extensions
        and path.is_file()
        and not any(path.is_relative_to(archive) for archive in archives)
    )
