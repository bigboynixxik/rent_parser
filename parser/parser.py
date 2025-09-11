import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua

from settings import URL, DEAL_TYPE, MAX_PRICE, MIN_PRICE, OFFER_TYPE, ROOM1, \
    ROOM2, PAGE, REGION


class Parser:
    def __init__(self):
        self.response = None
        self.page_num = 1
        self.data = []
        self.sorted_flat_data = []
        self.soup = None

        self.params = {DEAL_TYPE: 'rent',
                       MAX_PRICE: 40000,
                       MIN_PRICE: 10000,
                       OFFER_TYPE: 'flat',
                       ROOM1: 1,
                       ROOM2: 1,
                       PAGE: self.page_num,
                       REGION: 4827}
        self.user_agent = ua()
        self.headers = {'User-Agent': self.user_agent.chrome}
        self.data = []

    def _get_response(self):
        try:
            self.response = requests.get(
                URL,
                params=self.params,
                headers=self.headers,
                timeout=10)
        except requests.exceptions.RequestException as e:
            print(e, 'Хуйня с ссылкой?')
            self._get_response()

    def start_parsing(self):
        try:
            big_div = self.soup.find(attrs={'data-name': 'Offers'})
            divs = big_div.find_all('div', attrs={'data-testid': 'offer-card'})
            time.sleep(3)
            for div in divs:
                link = div.find('a')
                images = link.find_all('img')
                images_list = []
                for img in images:
                    images_list.append(img.get('src'))
                information = div.find_all('div', attrs={
                    'data-name': 'GeneralInfoSectionRowComponent'})
                flat_info = []
                for info in information:
                    some_text = info.text.split('\n')
                    if some_text == ['Только на Циан']:
                        continue
                    if some_text != ['']:
                        flat_info.append(some_text[0])
                    if some_text == ['']:
                        flat_info.append(link.get('href'))
                        flat_info.append(images_list)
                        self.data.append(flat_info)
                        flat_info = []
                images_list = []
        except Exception as e:
            print(e)
            time.sleep(1)
            self.parsing()

    def get_html(self):
        self._get_response()
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        time.sleep(5)

    def parsing(self):
        self.get_html()
        self.start_parsing()

    def work_with_data(self):
        """
        Метод для обработки данных, которые в последствии будут храниться
        :return:
        """
        flat_dict = {}
        for flat in self.data:
            flat_dict['flat_info'] = flat[0]
            flat_dict['flat_address'] = flat[1]
            flat_dict['flat_price'] = flat[2]
            flat_dict['flat_descript'] = flat[3]
            flat_dict['flat_link'] = flat[-2]
            flat_dict['flat_img'] = flat[-1]
            self.sorted_flat_data.append(flat_dict)
            flat_dict = {}
        for flat in self.sorted_flat_data:
            for key, value in flat.items():
                print(f'{key} - {value}')
            print(
                '================================================================\n')


parser = Parser()
parser.parsing()
parser.work_with_data()
