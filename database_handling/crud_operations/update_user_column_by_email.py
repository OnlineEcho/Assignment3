from database_classes.Users_Base import Users


def update_user_column_by_email(session, email, column, data):
    session.query(Users).filter(Users.email == email).update({column: data})
    session.commit()
