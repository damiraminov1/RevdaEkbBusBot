import re

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
        for div in soup.find_all('div', attrs={'class': 'su-spoiler-content su-u-clearfix su-u-trim'}).__reversed__():
            if 'Северный' in str(div) or 'Северного' in str(div):
                lst = div.text.split('\n')
                for m in lst:
                    if 'Ревда' in m or 'Ревды' in m:
                        data["from_revda"] = m
                    elif 'Северный' in m or 'Северного' in m:
                        data['from_ekb'] = m
                    else:
                        data['additional_information'] += '\n' + m
                data['full_schedule'] = data['from_revda'] + '\n' + data['from_ekb']
                data['status'] = 'success'
                return data
