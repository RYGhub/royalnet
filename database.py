import sqlalchemy.exc
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import bcrypt


class NoUsersMatchingError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


# Initialize the database
engine = create_engine("sqlite:///db.sqlite")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    royal = Column(Boolean, nullable=False)
    telegram_id = Column(Integer, unique=True)
    discord_id = Column(Integer, unique=True)
    diario_entries = relationship("Diario")

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Diario(Base):
    __tablename__ = "diario"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    author = Column(Integer, ForeignKey("members.id"))

    def __repr__(self):
        return f"<Diario {self.date} {self.text}>"

Base.metadata.create_all(engine)


def create_user(username, password, royal=False):
    """Create a new user and add it to the database."""
    # Create a new session
    session = Session()
    # Hash the password with bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
    # Create a new user
    new_member = User(username=username, password=hashed_password, royal=royal)
    # Add the newly created member to the session
    session.add(new_member)
    # Commit the changes
    session.commit()


# TODO: check for vulnerabilities
def change_password(username, newpassword):
    # Create a new session
    session = Session()
    # Hash the new password using bcrypt
    hashed_password = bcrypt.hashpw(newpassword.encode("utf8"), bcrypt.gensalt())
    # Find the user entry
    users = session.query(User).filter_by(username=username).all()
    if len(users) == 0:
        raise NoUsersMatchingError("No users with the specified username found.")
    db_user = users[0]
    # Change the password and commit
    db_user.password = hashed_password
    session.commit()


def login(username, password, enable_exceptions=False):
    """Try to login using the database password.
    The session is always returned, while the user object is returned if the login is successful."""
    # Create a new session
    session = Session()
    # Find the matching user
    db_user = session.query(User).filter_by(username=username).first()
    # Verify that the user exists
    if db_user is not None:
        return session, None
    # Test the password and return the session and the user if successful
    if bcrypt.hashpw(password.encode("utf8"), db_user.password) == db_user.password:
        return session, db_user
    else:
        if enable_exceptions:
            raise InvalidPasswordError("The specified password doesn't match the user's.")
        else:
            return session, None


def init_royal_db():
    create_user("test", "test", True)


def find_user(username):
    """Find the user with the specified username and return the session and the user object."""
    # Create a new session
    session = Session()
    # Find the matching user
    db_user = session.query(User).filter_by(username=username).first()
    # Return the session and the user
    return session, db_user


def migrate_diario():
    import datetime
    session = Session()
    file = open("diario.txt", encoding="utf8")
    for row in file:
        entry = row.split("|", 1)
        new = Diario()
        new.date = datetime.datetime.fromtimestamp(int(entry[0]))
        new.text = entry[1]
        session.add(new)
    session.commit()


def new_diario_entry(dt, text, author):
    # Create a new session
    session = Session()
    # Create a new diario entry
    entry = Diario()
    entry.date = dt
    entry.text = text
    entry.author = author.id
    # Add the entry to the database
    session.add(entry)
    # Commit the change
    session.commit()
