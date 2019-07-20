import sqlite3

class userDB:

    def __init__(self):
        self.conn = sqlite3.connect("USERS.db")
        self.mycursor = self.conn.cursor()

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
                    _ID INTEGER PRIMARY KEY,
                    USERNAME TEXT,
                    PASSWORD TEXT )""")

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS RELATIONSHIP (
                            id INTEGER PRIMARY KEY,
                            username_1 TEXT,
                            username_2 TEXT,
                            status TEXT )""")

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

    # Inserts a new relation
    def rela_insert(self, username1, username2):
        self.mycursor.execute("INSERT INTO RELATIONSHIP (username_1, username_2, status) VALUES (?,?,0)", (username1, username2) )
        self.conn.commit()

    # Accept friend request
    def accept_req(self, username1, username2):
        self.mycursor.execute("UPDATE relationship SET status = 1 WHERE username_1 = ? and username_2 = ?",
                              (username1, username2))

    # Decline friend request
    def decline_req(self, username1, username2):
        self.mycursor.execute("DELETE FROM relationship WHERE username_1 = ? and username_2 = ?",
                              (username1, username2))

    # Display friend list
    def get_friendList(self, username1):
        self.mycursor.execute("SELECT username FROM USERS "
                              "WHERE username IN "
                              "(SELECT username_2 FROM relationship WHERE username_1 = ? AND status = 1)"
                              " OR username IN "
                              "(SELECT username_1 FROM relationship WHERE username_2 = ? AND status = 1)",
                              (username1, username1))
        return self.mycursor.fetchall()

    # Display friend request list1
    def get_requestList(self, username2):
        self.mycursor.execute("SELECT username From USERS "
                              "WHERE username IN "
                              "(SELECT username_1 FROM relationship WHERE username_2 = ? AND status = 0)",
                              (username2) )
        return self.mycursor.fetchall()

