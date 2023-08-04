from __future__ import annotations

from changelog_modified_hook.check_changelog_modified import (
    find_changelog_in_added_files,
    main,
)
from changelog_modified_hook.util import cmd_output


def test_nothing_added(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert find_changelog_in_added_files(["f.py"]) == 1


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join("f.py").write("print('hello world')")
        cmd_output("git", "add", "f.py")

        assert find_changelog_in_added_files(["f.py", "CHANGELOG.md"]) == 1


def test_add_something_giant(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join("f.py").write("print('hello world')")
        temp_git_dir.join("CHANGELOG.md").write("print('hello world')")

        # Should not fail when not added
        assert find_changelog_in_added_files(["f.py"]) == 1

        cmd_output("git", "add", ".")

        assert find_changelog_in_added_files(["f.py", "CHANGELOG.md"]) == 0


def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 1

        temp_git_dir.join("f.py").write("print('hello world')")
        temp_git_dir.join("CHANGE.md").write("print('hello world')")

        # Should not fail when not added
        assert find_changelog_in_added_files(["f.py"]) == 1

        cmd_output("git", "add", ".")

        # Should fail with --maxkb
        assert (
            main(argv=["f.py", "CHANGE.md", "--changelog-name", "CHANGE.md"])
            == 0
        )
