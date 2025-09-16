import os
import subprocess  # noqa: B404
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery(stdout, *args, **kwargs):
    stdout.write("Restarting celery...")
    autoreload.raise_last_exception()
    subprocess.run(["/usr/bin/pkill", "-f", "bin/celery"], check=True)  # noqa: S603
    celery_path = os.path.join(os.path.dirname(sys.executable), "celery")
    subprocess.run([celery_path, "-A", "conf", "worker", "-l", "info"], check=True)  # noqa: S603, B603


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery, args=(self.stdout,), kwargs=None)
