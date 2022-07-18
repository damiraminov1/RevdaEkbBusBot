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
            return "Can't Parse!"

        data = list()
        for i in soup.find_all('div', attrs={'class': 'su-spoiler-content su-u-clearfix su-u-trim'}):
            if "От автовокзала «Северный»" in str(i) and "От автостанции Ревды" in str(i):
                lst = i.text.split('\n')
                data = {
                    'price': lst[1],
                    'from_revda': lst[2],
                    'from_ekb': lst[3],
                    'full_schedule': lst[2] + '\n' + lst[3],
                    'additional_information': lst[4]
                }
        return data
