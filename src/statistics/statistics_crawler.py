import re
import time
from math import ceil
import logging as log
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from src.constant import *
from src.statistics.statistics_class import Statistics


def get_to_statistics_page(driver):
    driver.get(STATISTICS_URL)
    close_flash_pop_up(driver)
    log_in(driver)
    log.info('In statistics page')




def crawl_statistics(driver):
    done = False
    stats = Statistics()

    try:
        with open(X12, 'a', encoding='utf-8') as x12:
            while not done:
                all_rows = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//td[contains(text(), "2019")]')))
                if stats.matches_total == 0:
                    log.info('{} matches to inspect'.format(len(all_rows)))
                if stats.matches_total == len(all_rows) - 1:
                    done = True
                # enter match details page
                link = all_rows[stats.matches_total].find_element_by_xpath('./following-sibling::td/a')
                match = link.text
                link.click()
                log.info('Inspecting match {}: {}'.format(stats.matches_total + 1, match))
                stats = inspect_match(driver, stats, x12)
                driver.execute_script("window.history.go(-1)")
                stats.matches_total += 1
    except Exception:
        raise
    finally:
        with open(INFO, 'a', encoding='utf-8') as info:
            info.write('Matches total: {}\n'.format(stats.matches_total))
            info.write('Matches     1: {}\n'.format(stats.matches_1))
            info.write('Matches     X: {}\n'.format(stats.matches_x))
            info.write('Matches     2: {}\n\n'.format(stats.matches_2))
            info.write('Max streak  1: {}\n'.format(stats.max_streak_1))
            info.write('Max streak  X: {}\n'.format(stats.max_streak_x))
            info.write('Max streak  2: {}\n\n'.format(stats.max_streak_2))
            info.write('Min     coef for X1: {}\n'.format(stats.min_coef_x1))
            info.write('Max     coef for X1: {}\n'.format(stats.max_coef_x1))
            info.write('Average coef for X1: {}\n\n'.format(round_up(stats.get_average_coef_x1(), 2)))
            info.write('Min     coef for X2: {}\n'.format(stats.min_coef_x2))
            info.write('Max     coef for X2: {}\n'.format(stats.max_coef_x2))
            info.write('Average coef for X2: {}\n'.format(round_up(stats.get_average_coef_x2(), 2)))




def log_in(driver):
    try:
        input_username = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.ID, 'HeaderPlaceHolder_HeaderControl_Login_Username')))
    except selenium.common.exceptions.TimeoutException:
        return

    input_password_click = driver.find_element_by_id('HeaderPlaceHolder_HeaderControl_Login_InitialPassword')
    input_password = driver.find_element_by_id('HeaderPlaceHolder_HeaderControl_Login_ProtectedPassword')
    ok_button = driver.find_element_by_id('HeaderPlaceHolder_HeaderControl_Login_Go')

    input_username.send_keys(USER)
    input_password_click.click()
    input_password.send_keys(PASS)
    ok_button.click()
    log.info('Logged in')




def close_flash_pop_up(driver):
    xpath = '//div[@id = "NoFlashPopupMessagePanel" and not(contains(@style, "display: none"))]/div/div[2]/table/tbody/tr[5]/td/table/tbody/tr/td/div/a'
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.XPATH, xpath))).click()




def inspect_match(driver, stats, x12):
    winner_table = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.XPATH, '//td[text() = "Победител в Мача"]')))

    winner_table.find_element_by_xpath('./following-sibling::td').click()

    winner = winner_table.find_element_by_xpath('../../tr[2]/td').text
    coef1 = float(winner_table.find_element_by_xpath('../../tr[2]/td[3]').text.replace(',', '.'))

    name2 = winner_table.find_element_by_xpath('../../tr[3]/td').text
    coef2 = float(winner_table.find_element_by_xpath('../../tr[3]/td[3]').text.replace(',', '.'))

    name3 = winner_table.find_element_by_xpath('../../tr[4]/td').text
    coef3 = float(winner_table.find_element_by_xpath('../../tr[4]/td[3]').text.replace(',', '.'))

    if winner == 'Равен':
        symbol = 'X'
        stats.matches_x += 1
        if stats.last == 'X':
            stats.streak_x += 1
        else:
            stats.streak_x = 1
        if stats.max_streak_x < stats.streak_x:
            stats.max_streak_x = stats.streak_x
        stats.last = 'X'
    elif (name2 == 'Равен' and coef1 < coef3) or (name3 == 'Равен' and coef1 < coef2):
        symbol = '1'
        stats.matches_1 += 1
        if stats.last == '1':
            stats.streak_1 += 1
        else:
            stats.streak_1 = 1
        if stats.max_streak_1 < stats.streak_1:
            stats.max_streak_1 = stats.streak_1
        stats.last = '1'
    else:
        symbol = '2'
        stats.matches_2 += 1
        if stats.last == '2':
            stats.streak_2 += 1
        else:
            stats.streak_2 = 1
        if stats.max_streak_2 < stats.streak_2:
            stats.max_streak_2 = stats.streak_2
        stats.last = '2'

    x12.write(symbol)


    if winner == 'Равен':
        if coef2 < coef3:
            one = name2
            two = name3
        else:
            one = name3
            two = name2
    elif name2 == 'Равен':
        if coef1 < coef3:
            one = winner
            two = name3
        else:
            one = name3
            two = winner
    else:
        if coef1 < coef2:
            one = winner
            two = name2
        else:
            one = name2
            two = winner

    double_table = driver.find_element_by_xpath('//td[text() = "Двоен Шанс"]')

    double_table.find_element_by_xpath('./following-sibling::td').click()

    double_name_1 = double_table.find_element_by_xpath('../following-sibling::tr/td').text
    double_coef_1 = float(double_table.find_element_by_xpath('../following-sibling::tr/td[3]').text.replace(',', '.'))

    double_name_2 = double_table.find_element_by_xpath('../following-sibling::tr/following-sibling::tr/td').text
    double_coef_2 = float(double_table.find_element_by_xpath('../following-sibling::tr/following-sibling::tr/td[3]').text.replace(',', '.'))

    double_name_3 = double_table.find_element_by_xpath('../following-sibling::tr/following-sibling::tr/following-sibling::tr/td').text
    double_coef_3 = float(double_table.find_element_by_xpath('../following-sibling::tr/following-sibling::tr/following-sibling::tr/td[3]').text.replace(',', '.'))

    if one in double_name_1 and two not in double_name_1:
        stats.sum_coef_x1 += double_coef_1
        if stats.min_coef_x1 > double_coef_1:
            stats.min_coef_x1 = double_coef_1
        if stats.max_coef_x1 < double_coef_1:
            stats.max_coef_x1 = double_coef_1
    elif one not in double_name_1 and two in double_name_1:
        stats.sum_coef_x2 += double_coef_1
        if stats.min_coef_x2 > double_coef_1:
            stats.min_coef_x2 = double_coef_1
        if stats.max_coef_x2 < double_coef_1:
            stats.max_coef_x2 = double_coef_1

    if one in double_name_2 and two not in double_name_2:
        stats.sum_coef_x1 += double_coef_2
        if stats.min_coef_x1 > double_coef_2:
            stats.min_coef_x1 = double_coef_2
        if stats.max_coef_x1 < double_coef_2:
            stats.max_coef_x1 = double_coef_2
    elif one not in double_name_2 and two in double_name_2:
        stats.sum_coef_x2 += double_coef_2
        if stats.min_coef_x2 > double_coef_2:
            stats.min_coef_x2 = double_coef_2
        if stats.max_coef_x2 < double_coef_2:
            stats.max_coef_x2 = double_coef_2

    if one in double_name_3 and two not in double_name_3:
        stats.sum_coef_x1 += double_coef_3
        if stats.min_coef_x1 > double_coef_3:
            stats.min_coef_x1 = double_coef_3
        if stats.max_coef_x1 < double_coef_3:
            stats.max_coef_x1 = double_coef_3
    elif one not in double_name_3 and two in double_name_3:
        stats.sum_coef_x2 += double_coef_3
        if stats.min_coef_x2 > double_coef_3:
            stats.min_coef_x2 = double_coef_3
        if stats.max_coef_x2 < double_coef_3:
            stats.max_coef_x2 = double_coef_3

    return stats




def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return ceil(n * multiplier) / multiplier












