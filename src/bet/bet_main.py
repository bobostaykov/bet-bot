import sys
import subprocess
import traceback
import logging as log
from os import path, makedirs
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))

try:
    from selenium import webdriver
except ImportError:
    print('\n\n---------- INSTALLING REQUIRED PACKAGES ----------\n\n')
    # log.info('INSTALLING REQUIRED PACKAGES')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    from selenium import webdriver

import src.bet.bet_crawler as crawler
from src.constant import *


def main():
    if not path.exists(LOG_DIR):
        makedirs(LOG_DIR)

    log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename=LOG_PATH, level=log.INFO)

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # you may need to specify executable_path='/usr/local/bin/chromedriver'
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        log.error('Chromedriver problem: ' + str(e))
        sys.exit()

    try:
        crawler.get_to_virtual_sports_page(driver)
        best_coef = crawler.find_best_coef(driver)
        crawler.bet(driver, best_coef)
    except Exception:
        log.error(traceback.format_exc())
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
