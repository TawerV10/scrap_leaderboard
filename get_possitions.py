from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import os

def visit_page(driver, count):
    try:
        tab = driver.find_element(By.XPATH, "//div[@id='tab-futures']")
        tab.click()
    except Exception as e:
        print(e)

    time.sleep(0.5)

    try:
        tab = driver.find_element(By.XPATH, "//body")
        for i in range(0, 10):
            tab.send_keys(Keys.DOWN)
    except Exception as e:
        print(e)

    time.sleep(0.5)

    try:
        menues = driver.find_elements(By.XPATH, "//div[@class='field css-vurnku']")

        menues[1].click()
        driver.find_elements(By.XPATH, "//div[@class='bn-sdd-dropdown showing css-fxluzf']/ul/li")[-1].click()

        menues[2].click()
        driver.find_elements(By.XPATH, "//div[@class='bn-sdd-dropdown showing css-fxluzf']/ul/li")[-1].click()
    except Exception as e:
        print(e)

    time.sleep(1)

    try:
        profiles = driver.find_elements(By.XPATH, "//div[@class='TraderCard css-vurnku']")
        profiles[count].click()
    except Exception as e:
        print(e)

def send_message(name, symbol, side, leverage, size, price, opened_time):
    year = int(opened_time.split(' ')[0].split('-')[0])
    month = int(opened_time.split(' ')[0].split('-')[1])
    day = int(opened_time.split(' ')[0].split('-')[2])
    hours = int(opened_time.split(' ')[1].split(':')[0])
    minutes = int(opened_time.split(' ')[1].split(':')[1])
    seconds = int(opened_time.split(' ')[1].split(':')[2])

    dtime = int(datetime(year, month, day, hours, minutes, seconds).timestamp())
    now = int(datetime.now().timestamp())

    if now - dtime <= 600:
        token = ''
        chat_id = ''

        side_str = 'side'
        if side == 'Long':
            side_str = 'LONG🟢'
        elif side == 'Short':
            side_str = 'SHORT🔴'

        message_text = f'🚨Alert🚨\n\n👨‍💻 Trader : {name}\n💎 Pair : {symbol}\n↕️ Side : {side_str}\n\n📈 Entry Price : {price}\n💰 Size : {size}\n✖️ Leverage : {leverage}'
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message_text}'
        r = requests.get(url)

def get_data(driver):
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    name = soup.find('div', class_='name css-8pbzgb').text
    positions = soup.find_all('tr', class_='bn-table-row bn-table-row-level-0')

    for position in positions:
        symbol = position.find('div', class_='symbol-name css-1c82c04').text.replace('Perpetual', '').strip()
        side = position.find('div', class_='symbol-detail css-4cffwv').find('div').text.strip()
        leverage = position.find('div', class_='leverage css-vurnku').text.strip()
        size = position.find_all('td', class_='bn-table-cell')[1].text.strip()
        price = position.find_all('td', class_='bn-table-cell')[2].text.strip()
        opened_time = position.find_all('td', class_='bn-table-cell')[5].text.strip()

        print(f'{name}: {symbol} {side} {leverage} - {size} - {price} - {opened_time}')
        send_message(name, symbol, side, leverage, size, price, opened_time)


def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    url = 'https://www.binance.com/en/futures-activity/leaderboard'
    driver.get(url)
    count = 1
    visit_page(driver, count)
    get_data(driver)

    driver.close()
    driver.quit()

if __name__ == '__main__':
    main()