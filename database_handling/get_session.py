from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    # Engine describe the SQLite database_operations to use and the connection URL
    engine = create_engine("sqlite:///users.sqlite")

    # Create a session maker (factory pattern)
    Session = sessionmaker(bind=engine)

    # Create a session using the session maker
    session = Session()

    return session