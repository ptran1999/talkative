import string

import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="chuoibuoi0tuoi",
    database="talkative",
)

mycursor = db.cursor()

userInsert = "INSERT INTO User (username, password) VALUES (%s, %s)"
usernameQuery = "SELECT * FROM User WHERE username = %s"
userQuery = "SELECT * FROM User WHERE username = %s AND password = %s"
