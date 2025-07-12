import requests
from fake_useragent import UserAgent as ua

from settings import URL, DEAL_TYPE, MAX_PRICE, MIN_PRICE, OFFER_TYPE, ROOM1, \
    ROOM2, ROOM3, PAGE

page_num = 1

params = {DEAL_TYPE: 'rent',
          MAX_PRICE: 40000,
          MIN_PRICE: 10000,
          OFFER_TYPE: 'flat',
          ROOM1: 1,
          ROOM2: 1,
          ROOM3: 1,
          PAGE: page_num}

user_agent = ua()
headers = {'User-Agent': user_agent.chrome}
try:
    response = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=10)
    print(response.url)
except requests.exceptions.RequestException as e:
    print(e)
