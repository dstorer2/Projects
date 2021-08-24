from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.address import Address



class RSVP:
    def __init__(self, data):
        self.id = data['id']
        self.event_id = data['event_id']
        self.user_id = data['user_id']

        self.event = []

    @classmethod
    def get_RSVPs(cls, data):
        query = "SELECT * FROM rsvps JOIN events ON rsvps.event_id = events.id JOIN users ON events.host_id = users.id JOIN addresses ON events.location = addresses.id WHERE rsvps.user_id = %(id)s"
        results = connectToMySQL("events_schema").query_db(query, data)

        rsvps = []

        for row_in_db in results:
            one_rsvp = cls(row_in_db)

            event_data = {
                "id": row_in_db['events.id'],
                "title": row_in_db['title'],
                "date": row_in_db['date'],
                "description": row_in_db['description'],
                "location": row_in_db['location'],
                "host_id": row_in_db['host_id']
            }

            location_data = {
                "id": row_in_db['addresses.id'],
                "street_address": row_in_db['street_address'],
                "city": row_in_db['city'],
                "state": row_in_db['state'],
                "zip": row_in_db['zip'],
            }

            host_data = {
                "id": row_in_db['users.id'],
                "first_name": row_in_db['first_name'],
                "last_name": row_in_db['last_name'],
                "email": row_in_db['email'],
                "password": row_in_db['password'],
                "address_id": row_in_db['address_id']
            }


            one_rsvp.event = Event(event_data)

            one_rsvp.event.location = Address(location_data)

            one_rsvp.event.host = User(host_data)

            rsvps.append(one_rsvp)
        return rsvps

    @classmethod
    def create_rsvp(cls, data):
        query = "INSERT INTO rsvps (event_id, user_id, created_at, updated_at) VALUES (%(event_id)s, %(user_id)s, now(), now())"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def check_rsvp(cls, data):
        query = "SELECT * FROM rsvps WHERE rsvps.event_id = %(event_id)s AND rsvps.user_id = %(user_id)s"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def delete_rsvp(cls, data):
        query = "DELETE FROM rsvps WHERE event_id = %(event_id)s AND user_id = %(user_id)s"
        return connectToMySQL('events_schema').query_db(query, data)
