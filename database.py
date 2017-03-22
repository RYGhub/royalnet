from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
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

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

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
    """Try to login using the database password. The session is always returned, while the user object is returned if the login is successful."""
    # Create a new session
    session = Session()
    # Find the matching user
    users = session.query(User).filter_by(username=username).all()
    # No user with a matching username found
    if len(users) == 0:
        if enable_exceptions:
            raise NoUsersMatchingError("No users with the specified username found.")
        else:
            return session, None
    db_user = users[0]
    # Test the password and return the session and the user if successful
    if bcrypt.hashpw(password.encode("utf8"), db_user.password) == db_user.password:
        # TODO: Maybe there's a better way to do this?
        return session, db_user
    else:
        if enable_exceptions:
            raise InvalidPasswordError("The specified password doesn't match the user's.")
        else:
            return session, None


def init_royal_db():
    create_user("steffo", "uno", True)
    create_user("adry", "due", True)
    create_user("cate", "tre", True)
    create_user("protoh", "quattro", True)
    create_user("infopz", "cinque", True)
    create_user("kappa", "sei", True)
    create_user("manu", "sette", True)
    create_user("frank", "otto", True)
    create_user("paltri", "nove", True)
    create_user("mestakes", "dieci", True)
    create_user("tauei", "undici", True)
    create_user("sensei", "dodici", True)
    create_user("gattopardo", "tredici", True)
    create_user("dima", "quattordici", True)
    create_user("spaggia", "quindici", True)
    create_user("igor", "sedici", True)
    create_user("nemesis", "diciassette", True)
    create_user("comiso", "diciotto", True)
    create_user("fulz", "diciannove", True)
    create_user("dailir", "venti", True)
    create_user("fedececco", "ventuno", True)
    create_user("albertwerk", "ventidue", True)
    create_user("voltaggio", "ventitre", True)
    create_user("doc", "ventiquattro", True)

if __name__ == "__main__":
    init_royal_db()