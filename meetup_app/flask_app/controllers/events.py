from flask_app.models.friendship import Friendship
from flask_app.models.event import Event
from flask_app.models.invite import Invite
from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route("/add_event")
def add_event():

    data = { "id": session['user_id']}

    friendships = Friendship.get_active_user_friends(data)

    return render_template("create_event.html", friendships = friendships)

@app.route("/create_event", methods=['POST'])
def create_event():


    data = {
        "title": request.form['title'],
        "date": request.form['date'],
        "description": request.form['description'],
        "location": request.form['location'],
        "host_id": session['user_id']
    }

    if not Event.validate_event(data):
        return redirect("/add_event")

    new_event = Event.create_event(data)

    return redirect('/event_success/'+str(new_event))

@app.route("/event_success/<int:event_id>")
def event_success(event_id):

    event_id = event_id

    return render_template("event_success.html", event_id = event_id)

@app.route("/view_event/<int:event_id>")
def view_event(event_id):

    data = { "event_id": event_id }

    event = Event.display_event_info(data)

    invites = Invite.get_event_invitees(data)
    print(invites)

    data1 = {
        "id": session['user_id']
    }

    user_friends = Friendship.get_active_user_friends(data1)


    return render_template("view_event.html", event = event, friends = user_friends, invites = invites)

