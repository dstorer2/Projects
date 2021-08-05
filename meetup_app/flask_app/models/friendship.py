from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash

class Friendship:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']

        self.friend = []

    @staticmethod
    def validate_friendship(data):
        is_valid = True
        if Friendship.find_friendship(data):
            flash("You guys are already friends!")
            is_valid = False
        return is_valid

    @classmethod
    def get_active_user_friends(cls, data):
        query = "SELECT * FROM friendships JOIN users AS friends ON friendships.friend_id = friends.id WHERE friendships.user_id = %(id)s"
        results = connectToMySQL('events_schema').query_db(query, data)

        friendships = []

        print(results)

        for row_in_db in results:
            one_friendship = cls(row_in_db)

            friend_data = {
                "id": row_in_db['friends.id'],
                "first_name": row_in_db['first_name'],
                "last_name": row_in_db['last_name'],
                "email": row_in_db['email'],
                "password": row_in_db['password'],
                "address_id": row_in_db['address_id'],
            }
            
            one_friendship.friend = User(friend_data)
            

            friendships.append(one_friendship)

        print(friendships)
        return friendships

    @classmethod
    def add_friendship(cls, data):
        query = "INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES (%(user_id)s, %(friend_id)s, now(), now())"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def find_friendship(cls, data):
        query = "SELECT * FROM friendships WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s"
        return connectToMySQL('events_schema').query_db(query, data)

