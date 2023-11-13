from flask import render_template, flash, redirect, url_for, session
import bcrypt
from database_handling.crud_operations.get_user_by_email import get_user_by_email


def login_page(db_session, request):
    user = get_user_by_email(db_session, request.form["email"])  # get user
    if user:  # if user exists
        if bcrypt.checkpw(request.form["password"].encode("utf-8"), user.password):  # check password
            session["email"] = request.form["email"]  # add email to flask session, passing to other route
            session["status"] = "logged in"
            return redirect(url_for("two_factor"))  # redirect to two-factor authentication page
    flash("Not Authenticated!")
    return render_template("login_page/login_page.html")
