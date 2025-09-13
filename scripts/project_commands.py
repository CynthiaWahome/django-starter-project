# Utility script for common project commands.
# Originally a workaround for Poetry; now used with uv.
import os
import sys
from subprocess import check_call


def server(*args) -> None:
    check_call([sys.executable, "manage.py", "runserver_plus", "0.0.0.0:8000"])  # noqa: S603


def tests() -> None:
    pytest_path = os.path.join(os.path.dirname(sys.executable), "pytest")
    check_call([pytest_path, "tests/"])  # noqa: S603


def worker() -> None:
    check_call([sys.executable, "manage.py", "celery_autoreload"])  # noqa: S603


def migrate() -> None:
    check_call([sys.executable, "manage.py", "migrate"])  # noqa: S603


def makemigrations() -> None:
    check_call([sys.executable, "manage.py", "makemigrations"])  # noqa: S603


def shell() -> None:
    check_call([sys.executable, "manage.py", "shell_plus"])  # noqa: S603
