from flask import Flask, request
import hashlib
import requests
from db import DataBase

app = Flask(__name__)

merchant_id = '33564'
secret_word = 'HP4Z.rSsu@]^Nyq'
secret_word2 = 'R}!2ZpJ8tk7O^pe'

db = DataBase('/home/db.db')

bot_token = "5966503898:AAFoEFDjEQ1YYcMisLnQYtwT58MN8QKdt2M"

class BotConfig:
    def __init__(self):
        self.param1 = None
        self.param2 = None
        self.param3 = None
        self.param4 = None
        self.param5 = None
        self.param6 = None
        self.param7 = None
        self.param8 = None
        self.param9 = None

    def load_from_database(self):
        config_data = db.get_bot_config()
        if config_data:
            self.param1 = config_data[1]
            self.param2 = config_data[2]
            self.param3 = config_data[3]
            self.param4 = config_data[4]
            self.param5 = config_data[5]
            self.param6 = config_data[6]
            self.param7 = config_data[7]
            self.param8 = config_data[8]
            self.param9 = config_data[9]

bot_config = BotConfig()
bot_config.load_from_database()

def send_message(chat_id, text, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            'keyboard': [
                [{'text': '🎴 Добавить пост'}, {'text': '🚦 Управление накруткой'}],
                [{'text': '💷 Управление арендой'}, {'text': '👥 Рефералы'}],
                [{'text': '📟 Инструкция'}]
            ],
            'resize_keyboard': True
        }
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        print("Сообщение отправлено в Telegram")
    else:
        print("Ошибка отправки сообщения в Telegram")

@app.route('/payment/notification', methods=['POST'])
def payment_notification():
    bot_config.load_from_database()
    amount = request.form.get('AMOUNT')
    order_id = request.form.get('MERCHANT_ORDER_ID')
    user_id = request.form.get('us_login')
    sign = request.form.get('SIGN')
    email = request.form.get('P_EMAIL')
    expected_sign_string = f"{merchant_id}:{amount}:{secret_word2}:{order_id}"
    expected_sign = hashlib.md5(expected_sign_string.encode()).hexdigest()
    if sign != expected_sign:
        return 'wrong sign', 400
    
    if not sign in db.find_sign():
        db.payment_save(user_id, sign, order_id, amount, email)
        send_message(user_id, "Оплата прошла успешно! Благодарим вас за доверие к нашему сервису ✅\n\n⌨️ Клавиатура обновлена.", bot_token)
        if amount == str(bot_config.param3):
            time = 86400
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param4):
            time = 86400 * 3
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param5):
            time = 86400 * 7
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param6):
            time = 2592000
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param7):
            time = 2592000 * 3
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param8):
            time = 2592000 * 6
            db.new_rent(user_id, 1, time)
        if amount == str(bot_config.param9):
            time = 2592000 * 12
            db.new_rent(user_id, 1, time)
        db.increment_count_rent()
    else:
        return 'this is an old operation.', 409
    return 'YES'

if __name__ == '__main__':
    app.run()