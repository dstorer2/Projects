from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.event import Event
from flask_app.models.user import User

class Invite:
    def __init__(self, data):
        self.id = data['id']
        self.event_id = data['event_id']
        self.invitee_id = data['invitee_id']
        self.status = data['status']

        self.event = []
        self.invitee = []

    @classmethod
    def send_invite(cls, data):
        query = "INSERT INTO invites (event_id, invitee_id, created_at, updated_at) VALUES (%(event_id)s, %(invitee_id)s, now(), now())"
        return connectToMySQL('events_schema').query_db(query, data)

    @classmethod
    def get_invites_for_user(cls, data):
        query = "SELECT * FROM invites JOIN events ON invites.event_id = events.id WHERE invitee_id = %(id)s"
        results = connectToMySQL('events_schema').query_db(query, data)

        if not results:
            return False

        invites = []
        for row_in_db in results:
            one_invite = cls(row_in_db)

            event_data = {
                "id": row_in_db['events.id'],
                "title": row_in_db['title'],
                "date": row_in_db['date'],
                "description": row_in_db['description'],
                "location": row_in_db['location'],
                "host_id": row_in_db['host_id'],
            }

            one_invite.event = Event(event_data)
            one_invite.event.host = User.get_host(event_data)

            invites.append(one_invite)

        return invites

    @classmethod
    def get_event_invitees(cls, data):
        query = "SELECT * FROM invites JOIN users ON invites.invitee_id = users.id WHERE invites.event_id = %(event_id)s"
        results = connectToMySQL('events_schema').query_db(query, data)
        print(results)
        if not results:
            return False

        invites = []

        for row_in_db in results:
            one_invite = cls(row_in_db)

            user_data = {
                "id": row_in_db['users.id'],
                "first_name": row_in_db['first_name'],
                "last_name": row_in_db['last_name'],
                "email": row_in_db['email'],
                "password":row_in_db['password'],
                "address_id": row_in_db['address_id'],
            }

            one_invite.invitee = User(user_data)

            invites.append(one_invite)

        return invites

    @classmethod
    def view_invite(cls, data):
        query = "SELECT * FROM invites JOIN events ON invites.event_id = events.id JOIN users ON events.host_id = users.id WHERE invites.id = %(id)s"
        result = connectToMySQL('events_schema').query_db(query, data)

        invite = cls(result[0])

        event_data = {
            "id": result[0]['events.id'],
            "title": result[0]['title'],
            "date": result[0]['date'],
            "description": result[0]['description'],
            "location": result[0]['location'],
            "host_id": result[0]['host_id'],
        }

        host_data = {
            "id": result[0]['users.id'],
            "first_name": result[0]['first_name'],
            "last_name": result[0]['last_name'],
            "email": result[0]['email'],
            "password": result[0]['password'],
            "address_id": result[0]['address_id'],
        }

        invite.event = Event(event_data)
        invite.event.host = User(host_data)

        return invite

    @classmethod
    def toggle_status(cls, data):
        query = "UPDATE invites SET status = %(status)s, updated_at = now() WHERE id = %(id)s"
        return connectToMySQL('events_schema').query_db(query, data)
