import bcrypt
from database_classes.Users_Base import Users
from database_handling.crud_operations.get_user_by_email import get_user_by_email


def add_user(session, request):

    if not get_user_by_email(session, request.form["email"]):
        new_user = Users(
            # emails should not be hashed as it would be impossible to contact users if needed
            # Encode, Hash and salt the password, set work factor/iterations of hashing process to take a few seconds
            email=request.form["email"],
            password=bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt(rounds=16))
        )

        session.add(new_user)
        session.commit()

        return new_user.email

    return False
