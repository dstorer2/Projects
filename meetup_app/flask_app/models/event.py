from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.address import Address



class Event:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.date = data['date']
        self.description = data['description']
        self.location = data['location']
        self.host_id = data['host_id']

        self.location = []
        self.host = []

    @staticmethod
    def validate_event(data):
        is_valid = True
        if data['location'] == 1:
            flash('Either you or the person you have selected to host do not have a valid address to host an event. Please update your address or change the location of your shindig to continue!')
            is_valid = False
        if len(data['description']) < 1:
            flash("Please add a description to your event!")
            is_valid = False
        if len(data['title']) < 1:
            flash("Please add a title to your event!")
            is_valid = False
        return is_valid

    @classmethod
    def create_event(cls, data):
        query = "INSERT INTO events (title, date, description, location, created_at, updated_at, host_id) VALUES (%(title)s, %(date)s, %(description)s, %(location)s, now(), now(), %(host_id)s)"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def display_event_info(cls, data):
        query = "SELECT * FROM events JOIN users ON events.host_id = users.id JOIN addresses ON events.location = addresses.id WHERE events.id = %(event_id)s"
        results = connectToMySQL('events_schema').query_db(query, data)

        event = cls(results[0])

        host_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "address_id": results[0]['address_id']
        }

        location_data = {
            "id": results[0]['addresses.id'],
            "street_address": results[0]['street_address'],
            "city": results[0]['city'],
            "state": results[0]['state'],
            "zip": results[0]['zip'],
        }
        event.host = User(host_data)
        event.location = Address(location_data)

        return event

    @classmethod
    def get_all_hosts_events(cls, data):
        query = "SELECT * FROM events WHERE host_id = %(id)s"
        return connectToMySQL('events_schema').query_db(query, data)



