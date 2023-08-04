from __future__ import annotations

import subprocess
from typing import Any


class CalledProcessError(RuntimeError):
    pass


def git_commit(*args, **kwargs):
    cmd = ("git", "commit", "--no-gpg-sign", "--no-verify", "--no-edit", *args)
    subprocess.check_call(cmd, **kwargs)


def added_files() -> set[str]:
    cmd = ("git", "diff", "--staged", "--name-only")
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: int | None = 0, **kwargs: Any) -> str:
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout
