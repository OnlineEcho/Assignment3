from flask import render_template, flash
from database_handling.crud_operations.add_user import add_user
from routes.create_user.add_twofa import add_twofa
from io import BytesIO
import base64


def create_user(session, request):

    if request.form["email"] and request.form["password"]:
        if add_user(session, request) == request.form["email"]:
            flash("Add Two Factor Authentication by scanning the QR code!")
            provisioning_uri, qr_code = add_twofa(session, request.form["email"])
            qr_code_bytes = BytesIO()
            qr_code.save(qr_code_bytes, format="PNG")
            encoded_qr_data = base64.b64encode(qr_code_bytes.getvalue())
            return render_template(
                "create_user/create_user.html",
                qr_code=encoded_qr_data
            )

    flash(f"Unable to create user with email: {request.form['email']}, user might already exist")
    return render_template("create_user/create_user.html")
