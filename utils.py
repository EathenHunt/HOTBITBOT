import requests
import time
import hmac
import hashlib
from urllib.parse import urljoin

HOTBIT_API_URL = "https://api.hotbit.io"


def get_unix_timestamp():
    """Returns the current Unix timestamp in milliseconds."""
    return int(time.time() * 1000)


def call_api(api_key, secret_key, method, endpoint, params=None, data=None):
    """Makes a signed API request to the Hotbit API."""
    url = urljoin(HOTBIT_API_URL, endpoint)
    timestamp = str(get_unix_timestamp())
    headers = {
        'HB-ACCESS-KEY': api_key,
        'HB-ACCESS-TIMESTAMP': timestamp,
    }
    if data:
        signature = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
        headers.update({'HB-ACCESS-SIGNATURE': signature})
    response = requests.request(method, url, headers=headers, params=params, json=data)
    return response.json()


def place_limit_order(api_key, secret_key, symbol, side, price, amount):
    """Places a limit order for a given trading pair."""
    endpoint = "/v1/order.put_limit"
    data = {'symbol': symbol, 'side': side, 'type': 'limit', 'price': str(price), 'amount': str(amount)}
    response = call_api(api_key, secret_key, 'POST', endpoint, data=data)
    if response['status'] == 'ok':
        return response['data']
    else:
        raise Exception(response['msg'])


def place_market_order(api_key, secret_key, symbol, side, amount):
    """Places a market order for a given trading pair."""
    endpoint = "/v1/order.put_market"
    data = {'symbol': symbol, 'side': side, 'type': 'market', 'amount': str(amount)}
    response = call_api(api_key, secret_key, 'POST', endpoint, data=data)
    if response['status'] == 'ok':
        return response['data']
    else:
        raise Exception(response['msg'])
