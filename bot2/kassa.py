import hashlib
import hmac
import requests
import json
import time

def get_balance(shop_id, nonce, api_key):
    url = 'https://api.freekassa.ru/v1/balance'
    
    # Генерация подписи
    data = {
        'shopId': shop_id,
        'nonce': nonce,
    }
    sorted_data = dict(sorted(data.items()))  # Сортировка данных по ключам
    sign_data = '|'.join([str(value) for value in sorted_data.values()])
    signature = hmac.new(api_key.encode(), sign_data.encode(), hashlib.sha256).hexdigest()
    
    data['signature'] = signature

    response = requests.post(url, json=data)

    if response.status_code == 200:
        json_data = response.json()
        balance_data = json_data.get('balance')
        if isinstance(balance_data, list) and len(balance_data) > 0:
            balance = balance_data[0].get('value')
            if balance is not None:
                return balance
    
    return None
