import requests

class Api:
    def __init__(self):
        self.api_url = 'https://n1panel.com/api/v2'
        self.api_key = '72943e41b5875bf554cac6849b4001fe'

    def order(self, data):
        post = {'key': self.api_key, 'action': 'add', **data}
        return self._connect(post)

    def status(self, order_id):
        post = {'key': self.api_key, 'action': 'status', 'order': order_id}
        return self._connect(post)

    def multiStatus(self, order_ids):
        post = {'key': self.api_key, 'action': 'status', 'orders': ','.join(map(str, order_ids))}
        return self._connect(post)

    def services(self):
        post = {'key': self.api_key, 'action': 'services'}
        return self._connect(post)

    def refill(self, order_id):
        post = {'key': self.api_key, 'order': order_id}
        return self._connect(post)

    def multiRefill(self, order_ids):
        post = {'key': self.api_key, 'orders': ','.join(map(str, order_ids))}
        return self._connect(post)

    def refillStatus(self, refill_id):
        post = {'key': self.api_key, 'refill': refill_id}
        return self._connect(post)

    def multiRefillStatus(self, refill_ids):
        post = {'key': self.api_key, 'refills': ','.join(map(str, refill_ids))}
        return self._connect(post)

    def balance(self):
        post = {'key': self.api_key, 'action': 'balance'}
        return self._connect(post)

    def _connect(self, post):
        response = requests.post(self.api_url, data=post)
        if response.status_code == 200:
            return response.json()
        else:
            return None