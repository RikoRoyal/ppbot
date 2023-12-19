import sqlite3
import datetime

class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def find_sign(self):
        with self.connection:
            result = self.cursor.execute("SELECT `sign` FROM `payment`").fetchall()
            all_signs = [row[0] for row in result] 
            return all_signs
        
    
    def payment_save(self, user_id, sign, order_id, amount, email):
        with self.connection:
            return self.cursor.execute("INSERT INTO `payment` (`user_id`, `sign`, `order_id`, `amount`, `email`) VALUES (?,?,?,?,?)",
                                       (user_id, sign, order_id, amount, email,))
    
    def check_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `rental_status` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()
        
    def date_rental(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `rental_time` FROM `users` WHERE `user_id`=?",(user_id,)).fetchone()
        
    def new_rent(self, user_id, rental_status, time):
        status = self.check_status(user_id)[0]
        if status != 1:
            now = datetime.datetime.now()
            rental_time = now.timestamp() + time
            with self.connection:
                self.cursor.execute("UPDATE `users` SET `rental_status` = ?, `rental_time` = ? WHERE `user_id` = ?", (rental_status, rental_time, user_id))
        else:
            rental_time = self.date_rental(user_id)[0] + time
            with self.connection:
                self.cursor.execute("UPDATE `users` SET `rental_status` = ?, `rental_time` = ? WHERE `user_id` = ?", (rental_status, rental_time, user_id))

    def get_bot_config(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM `config` WHERE `id` = 0")
            config_data = self.cursor.fetchone()
            return config_data
    
    def increment_count_rent(self):
        with self.connection:
            self.cursor.execute("UPDATE stats SET rent = rent + 1 WHERE id = 0")
            self.connection.commit()
