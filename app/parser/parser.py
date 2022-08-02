import requests
from bs4 import BeautifulSoup
from config import Config


class Parser:
    @staticmethod
    def _server_is_respond(html):
        return True if html.status_code == 200 else False

    @staticmethod
    def _get_html(url):
        html = requests.get(url, headers=Config.HEADERS)
        if Parser._server_is_respond(html):
            return html
        else:
            raise ConnectionError('Status code = {code}'.format(code=html.status_code))

    @staticmethod
    def get_content(url):
        try:
            soup = BeautifulSoup(Parser._get_html(url).text, 'html.parser')
        except ConnectionError:
            return {
                'status': 'failed'
            }
        data = {'price': str(),
                'from_revda': str(),
                'from_ekb': str(),
                'additional_information': str(),
                'status': str()}
        for i in soup.find_all('div', attrs={'class': 'su-spoiler-content su-u-clearfix su-u-trim'}):
            for j in ['Северный', 'Северного']:
                if j in str(i):
                    lst = i.text.split('\n')
                    for m in lst:
                        has_additional_info = True
                        for l in ['Цена', 'Рублей', 'цена', 'рублей']:
                            if l in m:
                                data['price'] = m
                                has_additional_info = False
                                continue
                        for l in ['Ревда', 'Ревды']:
                            if l in m:
                                data['from_revda'] = m
                                has_additional_info = False
                                continue
                        for l in ['Северный', 'Северного']:
                            if l in m:
                                data['from_ekb'] = m
                                has_additional_info = False
                                continue
                        if has_additional_info:
                            data['additional_information'] += '\n' + m
                    data['full_schedule'] = data['from_revda'] + '\n' + data['from_ekb']
                    data['status'] = 'success'
                    return data
