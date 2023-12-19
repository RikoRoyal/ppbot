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
        
    def channels_get(self):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM channels").fetchall()
            return data
        
    def get_all_id(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()
    
    def count_referes(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) FROM `users` WHERE `referer_id`=?",(user_id,)).fetchone()

    def stats_users(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(user_id) FROM `users`").fetchone()
    
    def date_rental(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `rental_time` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()
    
    def check_date(self, new_date):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `rental_time` <= ?", (new_date,)).fetchall()
            return result
    
    def check_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `rental_status` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()
        
    def update_entry(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `rental_status` = ?, `rental_time` = NULL WHERE `user_id` = ?", (0, user_id,))
            self.connection.commit()
    
    def count_post(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) FROM `post` WHERE `user_id`=?",(user_id,)).fetchone()
    
    def add_post(self, order_id, url, amount, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `post` (`order_id`,`url`,`amount`, `user_id`) VALUES (?,?,?,?)", (order_id, url, amount, user_id,))
    
    def get_orderId(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `order_id` FROM `post` WHERE `user_id`=?",(user_id,)).fetchall()
        
    def get_orderUrl(self, order_id):
        with self.connection:
            return self.cursor.execute("SELECT `url` FROM `post` WHERE `order_id`=?",(order_id,)).fetchall()
    
    def get_orderAll(self):
        with self.connection:
            return self.cursor.execute("SELECT `order_id` FROM `post`").fetchall()
    
    def delete_post(self, order_id):
        with self.connection:
            self.cursor.execute("DELETE FROM `post` WHERE `order_id`=?", (order_id,))
    
    def channels_save(self, name, id, url):
        with self.connection:
            return self.cursor.execute("INSERT INTO `channels` (`id_channel`, `name`, `url`) VALUES (?,?,?)",
                                       (name, id, url,))

    def channel_delete(self, channel_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `channels` WHERE `id_channel` = ?",(channel_id,))
    
    def update_rental(self, time, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `rental_status` = ?, `rental_time` = ? WHERE `user_id` = ?", (1, time, user_id))
            self.connection.commit()
    
    def get_bot_config(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM `config` WHERE `id` = 0")
            config_data = self.cursor.fetchone()
            return config_data
    
    def setState(self, state, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `state` = ? WHERE `user_id` = ?", (state, user_id))
            self.connection.commit()
    
    def getState(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `state` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()
    
    def updateConfig(self, column, value):
        with self.connection:
            query = f"UPDATE `config` SET `{column}` = ? WHERE `id` = 0"
            self.cursor.execute(query, (value,))
            self.connection.commit()
    
    def increment_count_post(self):
        with self.connection:
            self.cursor.execute("UPDATE stats SET count_post = count_post + 1 WHERE id = 0")
            self.connection.commit()

    def get_count_post(self):
        with self.connection:
            self.cursor.execute("SELECT count_post FROM stats WHERE id = 0")
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    
    def get_count_rent(self):
        with self.connection:
            self.cursor.execute("SELECT rent FROM stats WHERE id = 0")
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None