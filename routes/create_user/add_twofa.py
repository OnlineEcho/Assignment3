import pyotp
import qrcode
from database_handling.crud_operations.update_user_column_by_email import update_user_column_by_email


def add_twofa(session, email):
    # Generate the provisioning URI
    secret_key = pyotp.random_base32()  # Secret compatible with auth apps, base32
    totp = pyotp.TOTP(secret_key)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name="Authentication App")

    update_user_column_by_email(session, email, "secret_key", secret_key)

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)  # add the uri to the QR code
    qr.make(fit=True)  # generate the QR code based on the data

    img = qr.make_image(fill_color="black", back_color="white")  # make QR code an image

    return provisioning_uri, img
