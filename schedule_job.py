import schedule
import time

import crawl

def job():
    crawl.run()

def test_job():
    print("test")

schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
