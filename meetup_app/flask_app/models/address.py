from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash


import re
ADDRESS_REGEX = re.compile(r'\d{1,4}[A-Z]?\s([NSEW]\.)?\s(\d{1,3}(st|nd|rd|th))?\s(\w\s)+([A-Z][a-z]{1,3}\.)?')

class Address:
    def __init__(self, data):
        self.id = data['id']
        self.street_address = data['street_address']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']

        self.user = []

    @staticmethod
    def validate_address(data):
        is_valid = True
        if len(data['street_address'])<3:
            flash("Street address must be at least 3 characters long")
            is_valid = False
        if len(data['city'])<2:
            flash("City must be at least 2 characters long")
            is_valid = False
        if len(data['state'])<4:
            flash("Please enter full state name")
        if len(data['street_address'])<5:
            flash("Please enter address in format: ### Street Name St.")
            is_valid = False
        return is_valid

    @classmethod
    def get_user_address(cls, data):
        query = "SELECT * FROM addresses JOIN users ON addresses.id = users.address_id WHERE addresses.id = %(location)s"
        result = connectToMySQL('events_schema').query_db(query, data)

        address = cls(result[0])

        user_data = {
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": result['password'],
            "users.address_id": result['users.address_id'],
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at'],
        }

        address.user = User(user_data)

        return address

    @classmethod
    def create_address(cls, data):
        query = "INSERT INTO addresses (street_address, city, state, zip, created_at, updated_at) VALUES (%(street_address)s, %(city)s, %(state)s, %(zip)s, now(), now())"
        return connectToMySQL('events_schema').query_db(query, data)