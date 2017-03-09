from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

# Initialize the database
engine = create_engine("sqlite:///tempdb.sqlite")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    royal = Column(Boolean, nullable=False)

    def __str__(self):
        return f"{self.id} - {self.username}"

Base.metadata.create_all(engine)

def create_member(username, password, royal=False):
    """Create a new member and add it to the database."""
    # Create a new session
    session = Session()
    # Hash the password with bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
    # Create a new member
    new_member = Member(username=username, password=hashed_password, royal=royal)
    # Add the newly created member to the session
    session.add(new_member)
    # Commit the changes
    session.commit()

def login(username, password):
    """Try to login using the database password."""
    # Create a new session
    session = Session()
    # Find the matching user
    users = session.query(Member).filter(Member.username == username).all()
    # No user with a matching username found
    if len(users) == 0:
        return None
    else:
        db_user = users[0]
    # Test the password and return the user if successful
    if bcrypt.hashpw(password.encode("utf8"), db_user.password) == db_user.password:
        return db_user
    else:
        return None
