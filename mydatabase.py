import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="****",
    database="talkative",
)

mycursor = db.cursor()

userInsert = "INSERT INTO User (username, password) VALUES (%s, %s)"
usernameQuery = "SELECT * FROM User WHERE username = %s"
userQuery = "SELECT * FROM User WHERE username = %s AND password = %s"
relationshipQuery = "SELECT action_id FROM relationship WHERE (user1_ID = %s AND user2_ID = %s) OR (user2_ID = %s AND " \
                    "user1_ID = %s) "

getUserId = "SELECT id FROM User WHERE username = %s"
addFriend = "INSERT INTO relationship (user1_ID, user2_ID, status) VALUES (%s, %s, %s)"
acceptRequest = "UPDATE relationship SET status = 1 WHERE user1_ID = %s and user2_ID = %s"
declineRequest = "DELETE FROM relationship WHERE user1_ID = %s and user2_ID = %s;"
getFriendList = "SELECT username From User WHERE id IN (SELECT user2_ID FROM relationship WHERE user1_ID = %s AND " \
                "status = 1) OR id IN (SELECT user1_ID FROM relationship WHERE user2_ID = %s AND " \
                "status = 1)"
getFriendRequestList = "SELECT username From User WHERE id IN (SELECT user1_ID FROM relationship WHERE user2_ID = %s " \
                       "AND " \
                       "status = 0) "

