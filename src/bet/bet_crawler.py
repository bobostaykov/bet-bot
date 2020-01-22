import time
from math import ceil
import logging as log
import selenium
from datetime import datetime as dt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from src.constant import *



def get_to_virtual_sports_page(driver):
    driver.get(BET_HOME)
    driver.find_element_by_xpath('//*[@title="Спортни Залози"]').click()
    log_in(driver)
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[contains(text(), "Виртуални спортове")]'))).click()
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[contains(@class, "vr-VirtualsNavBarButton_Label") and contains(text(), "Футбол")]'))).click()
    log.info('In virtual football page')




def log_in(driver):
    try:
        login = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-Login')))
    except selenium.common.exceptions.TimeoutException:
        return

    input_fields = login.find_elements_by_css_selector('.hm-Login_InputField')
    ok_button = login.find_element_by_css_selector('.hm-Login_LoginBtn')

    input_fields[0].send_keys(USER)
    input_fields[1].click()
    input_fields[2].send_keys(PASS)
    ok_button.click()
    log.info('Logged in')

    try:
        pop_up_iframe = WebDriverWait(driver, 0).until(expected_conditions.presence_of_element_located((By.XPATH, '//iframe[@name = "ifunds"]')))
    except selenium.common.exceptions.TimeoutException:
        return
    driver.switch_to.frame(pop_up_iframe)
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.XPATH, '//a[@class = "btnc"]'))).click()




def find_best_coef(driver):
    xpath = '//*[contains(text(), "Двоен Шанс")]/../following-sibling::div/div/div/div[not(contains(@class, "Suspended") or contains(@class, "Dummy"))]'
    first_choice = WebDriverWait(driver, 180).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    first_coef = float(first_choice.find_element_by_xpath('./span/following-sibling::span').text)
    second_choice = first_choice.find_element_by_xpath('./following-sibling::div')
    second_coef = float(second_choice.find_element_by_xpath('./span/following-sibling::span').text)
    third_choice = second_choice.find_element_by_xpath('./following-sibling::div')
    third_coef = float(third_choice.find_element_by_xpath('./span/following-sibling::span').text)

    max_coef = max(first_coef, second_coef, third_coef)

    if max_coef == first_coef:
        first_choice.click()
        return first_coef
    if max_coef == second_coef:
        second_choice.click()
        return second_coef
    if max_coef == third_coef:
        third_choice.click()
        return third_coef




def bet(driver, initial_coef):
    coef = initial_coef
    # amount paid since last win
    amount_paid = 0
    lose_streak = 0
    win_streak = 0
    amount_to_bet = '0.25'
    if float(amount_to_bet) < PROFIT / (coef - 1):
        amount_to_bet = str(round_up(PROFIT / (coef - 1), 2))

    while True:
        old_balance_div = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-Balance ')))
        old_balance = float(old_balance_div.text.split()[0].replace(',', '.'))

        bet_iframe = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.XPATH, '//iframe[@name = "bsFrame"]')))
        driver.switch_to.frame(bet_iframe)

        input_bet = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.XPATH, '//input[@placeholder = "Залог"]')))
        input_bet.send_keys(amount_to_bet)

        minute = dt.now().minute
        second = dt.now().second

        wait_mins = 2 - (minute % 3)
        wait_secs = 20 - second
        wait = wait_mins * 60 + wait_secs
        if wait < 0:
            wait += 180
        time.sleep(wait)

        close_bet_frame(driver)
        # driver.find_element_by_xpath('//a[contains(@class, "placeBet")]').click()

        amount_paid += float(amount_to_bet)
        log.info(lose_streak * '  ' + '| Betting {}lv, amount paid since last win: {}lv'.format(amount_to_bet, amount_paid))

        driver.switch_to.default_content()
        refresh_balance(driver)

        new_balance_div = WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-Balance ')))
        new_balance = float(new_balance_div.text.split()[0].replace(',', '.'))

        coef = find_best_coef(driver)

        if new_balance > old_balance:
            win_streak += 1
            lose_streak = 0
            amount_paid = 0
            log.info('| We won, win streak: {}'.format(win_streak))
            amount_to_bet = '0.25'
            if float(amount_to_bet) < PROFIT / (coef - 1):
                amount_to_bet = str(round_up(PROFIT / (coef - 1), 2))
        else:
            lose_streak += 1
            win_streak = 0
            log.info(lose_streak * '  ' + '| We lost, lose streak: {}'.format(lose_streak))
            cumulative_profit = PROFIT + amount_paid
            amount_to_bet = str(round_up(cumulative_profit / (coef - 1), 2))




def refresh_balance(driver):
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-MembersInfoButton_AccountIcon '))).click()
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-BalanceDropDown_RefreshBalance '))).click()
    time.sleep(10)
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'hm-MembersInfoButton_AccountIcon '))).click()

            
            

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return ceil(n * multiplier) / multiplier




def close_bet_frame(driver):
    WebDriverWait(driver, WINDOW_WAIT_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'bs-Header_RemoveAllLink'))).click()







