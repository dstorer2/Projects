from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address_id = data['address_id']

        self.rsvp = []
        self.friendships = []


    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("Name must be at least 2 characters long")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Name must be at least 2 characters long")
            is_valid = False
        if len(data['password']) < 8:
            flash("Please enter a password that is at least 8 characters long")
            is_valid = False
        if data['password'] != data['conf_pass']:
            flash("Password and confirmation password do not match")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Must be valid email")
            is_valid = False
        return is_valid

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now())"
        results = connectToMySQL('events_schema').query_db(query, data)
        return results

    @classmethod
    def get_active_user_info(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('events_schema').query_db(query, data)
        print(result[0])
        return result[0]

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('events_schema').query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_host(cls, data):
        query = "SELECT * FROM users WHERE id = %(host_id)s"
        results = connectToMySQL('events_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_user_address(cls, data):
        query = "UPDATE users SET users.address_id = %(address_id)s WHERE users.id = %(id)s"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('events_schema').query_db(query)
        print(results)
        return results



