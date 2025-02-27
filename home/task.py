# from celery import shared_task
from home.models import Check
from manage_web.models import Web
from home.check import check_start
import time

def run_auto_check():
    # run the check every half an hour
    while True:
        check_start()
        print('Sleeping for half an hour...')
        time.sleep(1800)
        print('Waked up...')


