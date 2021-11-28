from selenium import webdriver
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.keys import Keys

from bondapp.req.reqconf import CHROME_DRIVER_PATH
from bondapp.req.kis import yld_by_rating, RATING_TYPE, get_date, KIS_URL
import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bondproject.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from bondapp.models import BondYld


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)

first_start = datetime.now()-relativedelta(years=5)

from bs4 import BeautifulSoup

def save_yld(start, present):
    if (start>present):
        return
    calendar_button = driver.find_element_by_name('startDt')
    calendar_button.clear()
    calendar_button.send_keys(start.strftime('%Y.%m.%d'))
    calendar_button.send_keys(Keys.ENTER)
    driver.find_element_by_id('btnSearch').click()
    # get_data 함수 실행
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dte = get_date(soup)
    for r in RATING_TYPE:
        data = yld_by_rating(soup, r)
        if not data: break
        BondYld(
            date=dte,
            bond_type=r,
            three_month=data['3m'],
            six_month=data['6m'],
            nine_month=data['9m'],
            one_year=data['1y'],
            one_year_half=data['1y6m'],
            two_year=data['2y'],
            three_year=data['3y'],
            five_year=data['5y']
        ).save()
    next_day = start + timedelta(days=1)
    return save_yld(next_day, present)


if __name__=='__main__':
    import sys
    sys.setrecursionlimit(18000)
    driver.implicitly_wait(3)
    driver.get(KIS_URL)
    save_yld(first_start, datetime.now())
