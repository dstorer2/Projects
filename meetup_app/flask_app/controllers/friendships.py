from flask_app.models.friendship import Friendship
from flask_app import app
from flask import render_template, redirect, request, session, flash



@app.route("/create_friendship", methods=['POST'])
def create_friendship():
    friendship_data = {
        "user_id": request.form['user_id'],
        "friend_id": request.form['friend_id']
    }

    if not Friendship.validate_friendship(request.form):
        return redirect('/add_friendship')

    Friendship.add_friendship(friendship_data)

    return redirect('/friendship_success')