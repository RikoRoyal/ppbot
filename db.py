import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` =?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.connection:
            if referer_id != None:
                return self.cursor.execute("INSERT INTO `users` (`user_id`,`referer_id`) VALUES (?,?)", (user_id,referer_id,))
            else:
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def get_all_id(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()

    def stats_users(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(user_id) FROM `users`").fetchone()

    def channels_save(self, name, id, url):
        with self.connection:
            return self.cursor.execute("INSERT INTO `channels` (`name`, `id`, `url`) VALUES (?,?,?)",
                                       (name, id, url,))

    def channels_get(self):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM channels").fetchall()
            return data

    def channel_delete(self, channel_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `channels` WHERE `id_channel` = ?",(channel_id,))

    def cc_save(self, photo, name, description, url):
        with self.connection:
            return self.cursor.execute("INSERT INTO `CC` (`photo`, `name`, `description`, `url`) VALUES (?,?,?,?)",
                                       (photo, name, description, url,))

    def cc_get(self):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM CC").fetchall()
            return data

    def cc_delete(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `CC` WHERE `id` = ?",(id,))

    def cc_result(self, id):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM `CC` WHERE `id` = ?",(id,)).fetchall()
            return data

    def get_balance(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()

    def get_balance_ref(self, referer_id):
        with self.connection:
            return self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id`=?",(referer_id,)).fetchone()

    def edit_balance_ref(self, edit_balance, referer_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `balance` = ? WHERE `user_id`=?",(edit_balance, referer_id,))

    def count_referes(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) FROM `users` WHERE `referer_id`=?",(user_id,)).fetchone()

    def edit_balance(self, edit_balance, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",(edit_balance, user_id,))

    def get_vipl(self):
        with self.connection:
            return self.cursor.execute("SELECT `vipl` FROM `stats`").fetchone()

    def edit_vipl(self, edit_vipl):
        with self.connection:
            return self.cursor.execute("UPDATE `stats` SET `vipl` = ?",(edit_vipl,))

    def get_data(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `data` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()

    def edit_data(self, edit_data, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `data` = ? WHERE `user_id` = ?",(edit_data, user_id,))

    def edit_config(self, editConfig):
        with self.connection:
            return self.cursor.execute("UPDATE `config` SET `ref_bonus` = ? WHERE `id` = 0",(editConfig,))

    def edit_configMin(self, editConfig):
        with self.connection:
            return self.cursor.execute("UPDATE `config` SET `Min_payOut` = ? WHERE `id` = 0",(editConfig,))

    def edit_url(self, url):
        with self.connection:
            return self.cursor.execute("UPDATE `study` SET `url` = ? WHERE `id` = 0",(url,))

    def get_urls(self):
        with self.connection:
            return self.cursor.execute("SELECT `url` FROM `study` WHERE `id`=0",()).fetchone()

    def get_refBonus(self):
        with self.connection:
            return self.cursor.execute("SELECT `ref_bonus` FROM `config` WHERE `id`=0",()).fetchone()

    def get_MinpayOUt(self):
        with self.connection:
            return self.cursor.execute("SELECT `min_payOut` FROM `config` WHERE `id`=0",()).fetchone()

    def add_output(self, user_id, amounts, wallet):
        with self.connection:
            return self.cursor.execute("INSERT INTO `output` (`user_id`,`summa`, `wallet`, `status`) VALUES (?,?,?,?)", (user_id, amounts, wallet, 'False'))

    def get_output(self):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM `output` WHERE `status` = 'False'",()).fetchall()
            return data

    def accept_vipl(self, id):
        with self.connection:
            return self.cursor.execute("UPDATE `output` SET `status` = True WHERE `id` = ?",(id,))

    def get_accept(self, id):
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `output` WHERE `id`=?",(id,)).fetchone()

    def returs_vipl(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `output` WHERE `id` = ?",(id,))
