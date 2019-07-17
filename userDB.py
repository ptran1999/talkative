import sqlite3

class userDB:

    def __init__(self):
        self.conn = sqlite3.connect("USERS.db")
        self.mycursor = self.conn.cursor()

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
                    _ID INTEGER PRIMARY KEY,
                    USERNAME TEXT,
                    PASSWORD TEXT )""")

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS FRIENDS (
                    _ID INTEGER PRIMARY KEY,
                    USERA TEXT,
                    USERB TEXT,
                    STATUS INTEGER
                     )""")

    # Inserts a new user into the database
    def user_insert(self, username, password):
        self.mycursor.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?,?)", (username,password) )
        self.conn.commit()

    # Searches a for a username in the the database
    def username_query(self, username):
        self.mycursor.execute("SELECT * FROM USERS WHERE USERNAME =?", (username, ))
        return self.mycursor.fetchall()

    # Searches for a user with the specified username and password
    def user_query(self, username, password):
        self.mycursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                              (username, password))
        return self.mycursor.fetchall()

    # Get User ID
    def get_user_id(self, username):

        self.mycursor.execute("SELECT _ID FROM USERS WHERE USERNAME = ?",
                              (username, ))
        return self.mycursor.fetchall()

    # TODO Implement all friends functions



