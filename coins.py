import os
from binance.spot import Spot as Client
import asyncio
import re
import requests
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient
import ast
import time
from pycoingecko import CoinGeckoAPI

client_spot = Client(key='gKh35K47HbgRpkW1mW89rvk7iuAPDpNaBSautbZOiPro100QTOtuWwDV4Ntlt6k8', secret='VqfBxewbcFraMqQF6UkJMLsTiZa2OPFTHLoxGEUk7xTWufmtox1BJFO3mTLgsrzJ', base_url='https://api.binance.com')
cg = CoinGeckoAPI()

recvWindow = 50000


a = [i['asset'] for i in client_spot.account(recvWindow=recvWindow)['balances']]
a = [i.lower() for i in a if not i.endswith('DOWN') and not i.endswith('UP') and not i.endswith('BULL') and not i.endswith('BEAR')]
print(a)
quit()

with open(os.path.join('/Users/zibo/fun/crypto/data', 'coin_names'), 'r') as coin_names:
	coingecko_token_names = [eval(i) for i in coin_names.read().strip().split('\n')]



b = []
for coin in a:
  for key in coingecko_token_names:
    if coin == key['symbol']:
      b.append(key['id'])
      break
      
      

