from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.address import Address
from flask_app.models.user import User


@app.route("/edit_address")
def edit_address():

    return render_template("edit_address.html")

@app.route("/update_address", methods=['POST'])
def update_address():

    data = {
        "street_address": request.form['street_address'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zip": request.form['zip'],
    }

    if not Address.validate_address(data):
        return redirect("/edit_address")

    new_address = Address.create_address(data)

    data2 = {
        "address_id": new_address,
        "id": session['user_id']
    }

    User.update_user_address(data2)

    return redirect('/dashboard')
