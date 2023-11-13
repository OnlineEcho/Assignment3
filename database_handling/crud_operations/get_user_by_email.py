from database_classes.Users_Base import Users


def get_user_by_email(session, email):
    user_by_email = session.query(Users).filter(Users.email == email).first()

    if user_by_email is None:
        return False

    return user_by_email
