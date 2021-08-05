from flask_app.models.friendship import Friendship
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.invite import Invite
from flask_app.models.rsvp import RSVP

@app.route("/send_invite", methods=['POST'])
def send_invite():

    data = {
        "event_id": request.form['event_id'],
        "invitee_id": request.form['invitee']
    }

    Invite.send_invite(data)

    return redirect("/invite_success/"+str(request.form['event_id']))

@app.route("/invite_success/<int:event_id>")
def invite_success(event_id):

    event_id = event_id

    return render_template("invite_success.html", event_id = event_id)

@app.route("/view_invite/<int:invite_id>")
def view_invite(invite_id):

    data = {
        "id": invite_id
    }

    invite = Invite.view_invite(data)

    return render_template("view_invite.html", invite = invite)

@app.route("/toggle_invite", methods=['POST'])
def toggle_invite():

    data = {
        "id": request.form['invite_id'],
        "status": request.form['status']
    }

    Invite.toggle_status(data)

    if request.form['status'] == "accept":

        data = {
            "event_id": request.form['event_id'],
            "user_id": session['user_id']
        }
        RSVP.create_rsvp(data)
    
    elif request.form['status'] == "decline":
        data = {
            "event_id": request.form['event_id'],
            "user_id": session['user_id']
        }
        if RSVP.check_rsvp(data):
            RSVP.delete_rsvp(data)

    else:
        data = {
            "event_id": request.form['event_id'],
            "user_id": session['user_id']
        }
        if RSVP.check_rsvp(data):
            RSVP.delete_rsvp(data)

    status = request.form['status']

    return redirect("/toggle_success/"+str(status))

@app.route("/toggle_success/<string:status>")
def toggle_success(status):
    
    status = status

    return render_template("invite_toggle_success.html", status = status)