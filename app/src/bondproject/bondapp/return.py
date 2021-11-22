import requests
from bs4 import BeautifulSoup

_url = 'https://www.kisrating.co.kr/ratingsStatistics/statics_spread.do'
_response = requests.get(_url)

def return_by_rating(search_title):
    key_data = [
        '구분', '3m', '6m', '9m', '1y', '1y6m', '2y', '3y', '5y'
    ]

    if _response.status_code == 200:
        html = _response.text
        soup = BeautifulSoup(html, 'html.parser')

        date = get_date()
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
            i+=1
        return dct_data

    else:
        print(_response.status_code)


def get_date():
    html = _response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('input', {'title':'기간선택'}).get('value')


if __name__=='__main__':
    import pandas as pd
    df = pd.DataFrame(return_by_rating('국고채'), index=['date'])
    df.set_index(['date'], inplace=True)
    print(df)
