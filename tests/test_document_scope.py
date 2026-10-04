import subprocess

import pytest

from scripts import check_markdown_links, check_markdown_math, document_scope


def test_only_registered_archives_and_git_ignored_files_are_excluded(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "project.yml").write_text(
        "paths:\n  docs_dir: knowledge\n"
        "documentation:\n  archived_paths:\n"
        "    - knowledge/discussions/imported.md\n"
        "    - knowledge/notebooks/downloads\n"
        "    - studies/example/frozen\n"
    )
    (tmp_path / ".gitignore").write_text("ignored/\n")
    archived = [
        "knowledge/discussions/imported.md",
        "knowledge/notebooks/downloads/source.ipynb",
        "studies/example/frozen/source.md",
    ]
    maintained = [
        "knowledge/discussions/README.md",
        "knowledge/notebooks/README.md",
        "studies/example/README.md",
        "studies/example/frozen-copy/notes.md",
        "experiments/exp001_example/requirements.md",
    ]
    for name in archived + maintained + ["ignored/generated.md"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[missing](missing.md)\n")
    subprocess.run(["git", "add", maintained[0]], cwd=tmp_path, check=True)
    selected = document_scope.maintained_documents(tmp_path, {".md", ".ipynb"})
    assert {path.relative_to(tmp_path).as_posix() for path in selected} == set(maintained)
    monkeypatch.setattr(check_markdown_links, "ROOT", tmp_path)
    errors = check_markdown_links.broken_links()
    assert len(errors) == len(maintained)
    assert any("requirements.md" in error for error in errors)
    monkeypatch.setattr(check_markdown_math, "ROOT", tmp_path)
    assert check_markdown_math.default_paths() == selected
    source = tmp_path / archived[0]
    source.write_text("$$x=y$$\n")
    assert check_markdown_math.main([str(source)]) == 1


@pytest.mark.parametrize("entries", ["docs", [".."], ["."], ["/tmp"], ["docs/*"], [None]])
def test_invalid_archive_config_fails_instead_of_hiding_documents(tmp_path, entries):
    with pytest.raises(ValueError, match="documentation.archived_paths"):
        document_scope.archived_document_paths(
            {"documentation": {"archived_paths": entries}}, tmp_path
        )


def test_archive_config_is_optional_for_existing_projects(tmp_path):
    assert document_scope.archived_document_paths({}, tmp_path) == []
