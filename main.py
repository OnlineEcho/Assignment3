from flask import Flask, request, render_template, session, Response
import os
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database_handling.get_session import get_session
from routes.login_page.login_page import login_page
from routes.create_user.create_user import create_user
from routes.twofa_user.twofa_user import twofa_user

app = Flask("Authentication App", template_folder='routes')
app.secret_key = os.urandom(24)  # session handling
csp = {
    'default-src': 'self',
    'style-src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css',
    'img-src': 'data:',
}
Talisman(app, content_security_policy=csp)
limiter = Limiter(  # rate limit
    get_remote_address,
    app=app,
    default_limits=["30/day"]
)
db_session = get_session()  # Get database session


@app.route("/", methods=["GET", "POST"])  # Login page
@limiter.limit("3/5 minute")  # add rate limit to login page
def index():
    if request.method == "POST":
        return login_page(db_session, request)
    else:
        return render_template("login_page/login_page.html")


@app.route("/two_factor", methods=["GET", "POST"])
def two_factor():
    if request.method == "POST":
        return twofa_user(db_session, request)
    else:
        if len(session) < 1:  # if user isn't authorized or has an email
            return Response(response="401 Unauthorized", status=401)
        elif session["email"] and session["status"] == "logged in":
            return render_template("twofa_user/twofa_user.html")


@app.route("/authenticated", methods=["GET"])
def authenticated():
    if len(session) < 1:  # if user isn't authorized
        return Response(response="401 Unauthorized", status=401)
    elif session["status"] == "authorized":
        return render_template("authenticated/authenticated.html")


@app.route("/create_user", methods=["GET", "POST"])  # Create user page
def create():
    if request.method == "POST":
        return create_user(db_session, request)
    else:
        return render_template("create_user/create_user.html")


if __name__ == "__main__":
    app.run(debug=True)  # ssl_context='adhoc'
