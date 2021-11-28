import requests
from bs4 import BeautifulSoup

KIS_URL = 'https://www.kisrating.co.kr/ratingsStatistics/statics_spread.do'
RATING_TYPE = [
    '국고채', 'AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-'
]

def yld_by_rating(soup, search_title):
    key_data = [
        '구분', '3m', '6m', '9m', '1y', '1y6m', '2y', '3y', '5y'
    ]

    date = get_date(soup)
    tbody = soup.select_one('tbody')
    tables = tbody.select('tr')
    titles = tbody.select('tr > td.fc_blue_dk')

    dct_data = {'date': date}
    i=0
    for title in titles:
        if title.get_text()==search_title:
            j=0
            for key in key_data:
                dct_data[key] = tables[i].select('td')[j].get_text()
                j+=1
            return dct_data
        i+=1
    return False


def get_date(soup):
    return soup.find('input', {'title':'기간선택'}).get('value')


def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)
