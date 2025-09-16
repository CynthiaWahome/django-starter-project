import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def task_dummy(arg_a: object, arg_b: object) -> None:
    logger.info(f"Called task_dummy with a:{arg_a} b:{arg_b}")
