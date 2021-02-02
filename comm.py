""" This module manage:
- Bit coin comunication and data format with CoinMakerCap API https://coinmarketcap.com/api/
- IFTTT Service comunication (information to mobile) https://ifttt.com/home
"""
"TODO: manejar la lista de informaciones con busqueda automatica"
import requests
from requests import Request, Session
import json

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/chbJqdWxbCqnuMR2gwGD0XTxVH8-qsu2yWU7_bTnn5x'
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' 

def get_btdata(cur):
    """ Json BT_info is:
            "price": 6602.60701122,
            "volume_24h": 4314444687.5194,
            "percent_change_1h": 0.988615,
            "percent_change_24h": 4.37185,
            "percent_change_7d": -12.1352,
            "market_cap": 113563929433.21645,
            "last_updated": "2018-08-09T21:56:28.000Z
    """
    parameters = {
    'symbol':'BTC',
    'convert':cur
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7351d04f-329e-4748-b137-28d0079459cb',
    }

    try: 
        session = Session()
        session.headers.update(headers)
        response = session.get(BITCOIN_API_URL, params=parameters)
        if response.status_code == 200:
            response_json = response.json()
            response = response_json["data"]['BTC']['quote'][cur]
            return True, response
        else:
            return False, response
    
    except requests.exceptions.RequestException:
        raise ConnectionError ('Error While trying to connect to BitCoin URL..') 
       
    
def post_IFTTT_event(event, bc_data):
    # Make sure that your key is in the URL
    data = {
        'value1':"{0:,.2f}".format(bc_data['price']), 
        'value2':"{0:.2%}".format(bc_data['percent_change_24h']/100), 
        'value3':"{0:.2%}".format(bc_data['percent_change_7d']/100)
        }
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    try:
        response = requests.post(ifttt_event_url, json=data) 
        if response.status_code == 200:
            response = 'IFTTT'
            return True , response
        else:
            #print('Error while sending IFTTT request: {}'.format(response))
            return False , response

    except requests.exceptions.RequestException as err:
        raise ConnectionError ('Error While trying to connect to IFTTT URL..'+ err)         
    

