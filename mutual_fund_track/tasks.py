from celery import task
from celery.utils.log import get_task_logger
# from celery.contrib import rdb
from mutual_fund_track.utils import *

logger = get_task_logger(__name__)

@task()
def task_save_new_mutual_funds():
    """
    downloads latest mutual funds file from given url
    """
    mutual_funds_in_file = download_mutual_fund_file()
    print(mutual_funds_in_file)
    logger.info("Data downloaded from url")

    mutual_funds_in_db = get_mutual_funds_from_db()
    print(mutual_funds_in_db)
    logger.info("Got all mutual funds from db")

    # rdb.set_trace()
    save_new_mutual_funds_db(mutual_funds_in_db, mutual_funds_in_file)
    logger.info("Saved new recordes to db")


@task()
def update_mutual_fund_values():
    save_new_mutual_fund_values(logger)
    logger.info("updated new fund values in db")
