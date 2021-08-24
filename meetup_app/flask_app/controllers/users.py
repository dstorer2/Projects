from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.rsvp import RSVP
from flask_app.models.invite import Invite
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route("/")
def index():
    return render_template("index.html")


#==============================REGISTER=============================

@app.route("/register", methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect("/")

    if User.get_by_email(request.form['email']):
        flash('Email already exists! Please login.')
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
    }

    new_user = User.new_user(data)

    session['user_id'] = int(new_user)

    return redirect("/dashboard")

#=================================LOGIN===================================

@app.route("/login", methods=['POST'])
def login():

    data = { "email": request.form['email'] }
    print(request.form)
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Email/password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/password")
        return redirect("/")

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['email'] = user_in_db.email
    session['address_id'] = user_in_db.address_id

    return redirect("/dashboard")

#===========================LOGOFF=========================

@app.route("/logoff")
def logoff():

    session.clear()

    return redirect("/")

#================================DASHBOARD==============================

@app.route("/dashboard")
def dashboard():

    if not session:
        flash("DON'T DO THAT")
        return redirect('/')

    data = { "id": session['user_id']}

    user = User.get_active_user_info(data)
    print(user)

    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    session['email'] = user['email']
    session['address_id'] = user['address_id']

    events = Event.get_all_hosts_events(data)

    rsvps = RSVP.get_RSVPs(data)

    invites = Invite.get_invites_for_user(data)

    return render_template("dashboard.html", user = user, rsvps = rsvps, invites = invites, events = events)

#==========================FRIENDSHIPS==========================

@app.route('/add_friendship')
def add_friendship():

    all_users = User.get_all_users()

    return render_template("add_friendship.html", all_users = all_users)

@app.route('/friendship_success')
def frienship_success():

    return render_template("friendship_success.html")

