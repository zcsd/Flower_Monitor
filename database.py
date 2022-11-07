import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector

class Database:
    def __init__(self, host, database, user, password):
        load_dotenv()
        # connect to Planetscale MySQL server
        try:
            self.mydb = mysql.connector.connect(
                host = host,
                database = database,
                user = user,
                password = password,
                ssl_ca="/etc/ssl/certs/ca-certificates.crt"
            )
            if self.mydb.is_connected():
                print("Connected to DB server successfully.")
                self.cursor = self.mydb.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def insert_env_data(self, now, data):
        try:
            # data = [last_filename, temperature, humidity, lux]
            values = (now.strftime("%Y%m%d%H%M%S"), now.strftime("%Y_%m_%d"), now.strftime("%H_%M"), data[0], data[1], data[2], data[3])
            self.cursor.execute("INSERT INTO flowerenv (`id`, `day`, `hourmin`, `filedir`, `temperature`, `humidity`, `lux`) VALUES (%s, %s, %s, %s, %s, %s, %s)", values)
            self.mydb.commit()
            if self.cursor.rowcount > 0:
                print("Inserted env data to DB successfully.")
        except Error as e:
            print("Error while inserting to MySQL", e)
            # Planetscale MySQL lose connection error
            print("Trying to reconnect to DB server...")
            self.mydb.reconnect(attempts=3)
            if self.mydb.is_connected():
                print("Reconnected to DB server successfully.")
                self.cursor = self.mydb.cursor()
                self.insert_env_data(now, data)

    def close_connection(self):
        if self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()
