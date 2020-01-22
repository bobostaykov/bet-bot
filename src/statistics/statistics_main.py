#! /usr/bin/env python3

import sys
import os
import time
import subprocess
import traceback
import logging as log
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))

import src.statistics.statistics_crawler as crawler
from src.constant import *

try:
    from selenium import webdriver
except ImportError:
    print('\n\n---------- INSTALLING REQUIRED PACKAGES ----------\n\n')
    # log.info('INSTALLING REQUIRED PACKAGES')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    from selenium import webdriver


def main():
    if os.path.isfile(STATS_LOG):
        os.remove(STATS_LOG)
    if os.path.isfile(INFO):
        os.remove(INFO)
    if os.path.isfile(X12):
        os.remove(X12)

    log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename=STATS_LOG, level=log.INFO)

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # you may need to specify executable_path='/usr/local/bin/chromedriver'
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print('Chromedriver problem: ' + str(e))
        sys.exit()

    begin = time.time()

    try:
        crawler.get_to_statistics_page(driver)
        crawler.crawl_statistics(driver)
    except Exception:
        log.error(traceback.format_exc())
    finally:
        total_time = time.time() - begin
        if total_time / 60 < 60:
            log.info('%.2f minutes\n' % (total_time / 60))
        else:
            log.info('%.2f hours\n' % (total_time / 3600))
        driver.quit()


if __name__ == '__main__':
    main()