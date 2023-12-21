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
        # try:
        #     soup = BeautifulSoup(Parser._get_html(url).text, 'html.parser')
        # except ConnectionError:
        #     return {
        #         'status': 'failed'
        #     }
        # data = {'price': str(),
        #         'from_revda': str(),
        #         'from_ekb': str(),
        #         'additional_information': str(),
        #         'status': str()}

        data = {
            "from_revda": 'От автостанции Ревды:  6:00, 6:20, 6:55, 7:25, 8:15, 8:40*, 9:05, 10:30, 11:30, 12:20, 13:00*, 13:40, 15:00, 16:20*, 16:45, 17:40, 18:40, 20:30',
            'from_ekb': 'От автовокзала «Северный»: 7:25, 7:55, 8:55, 9:45, 10:15*, 11:05, 11:35, 13:05, 13:50, 14:15, 14:35*, 15:55, 16:40, 17:55*, 18:15, 19:15, 20:15, 22:05',
            'additional_information': 'Цена: 138 рублей \n * — рейсы междугороднего маршрута № 651/66 «Ледянка — Екатеринбург», на которых имеют право бесплатного проезда областные и федеральные льготные категории граждан, имеющие прописку в Свердловской области: Цена без льгот — 150 рублей.',
            'status': 'success',
        }
        data["full_schedule"] = data['from_revda'] + '\n' + data['from_ekb']

        # for div in soup.find_all('div', attrs={'class': 'su-spoiler-content su-u-clearfix su-u-trim'}).__reversed__():
        #     if 'Северный' in str(div) or 'Северного' in str(div):
        #         lst = div.text.split('\n')
        #         for m in lst:
        #             if 'Ревда' in m or 'Ревды' in m:
        #                 data["from_revda"] = m
        #             elif 'Северный' in m or 'Северного' in m:
        #                 data['from_ekb'] = m
        #             else:
        #                 data['additional_information'] += '\n' + m
        #         data['full_schedule'] = data['from_revda'] + '\n' + data['from_ekb']
        #         data['status'] = 'success'
        return data
