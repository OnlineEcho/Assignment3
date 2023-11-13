from flask import render_template, flash, redirect, url_for, session
import pyotp
from database_handling.crud_operations.get_user_by_email import get_user_by_email


def twofa_user(db_session, request):
    user = get_user_by_email(db_session, session["email"])  # get user
    if request.form["twofa"]:  # read 2fa input
        totp = pyotp.TOTP(user.secret_key)  # generate totp based on users' secret key
        key_now = totp.now()
        if request.form["twofa"] == key_now:  # check if they are the same
            session["status"] = "authorized"
            return redirect(url_for("authenticated"))  # if correct authenticate user
        else:  # if incorrect, redirect to log in page again.
            flash("Two-Factor Time-Based One Time Password incorrect!")
    return redirect(url_for("index"))
