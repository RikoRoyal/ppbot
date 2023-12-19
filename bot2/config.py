from utils.db import DataBase

db = DataBase('db.db')

bot_token = "5966503898:AAFoEFDjEQ1YYcMisLnQYtwT58MN8QKdt2M"

admins = [395701818, 672468872, 793825239]

BOT_NICKNAME = "TOPTGTOP_bot"

not_sub_message = "Вы должны подписаться на все каналы"

merchant_id = '33564'
secret_word = 'HP4Z.rSsu@]^Nyq'
api_key = '2c74f8ba1b5ddb49d546bff27d905dbe'

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