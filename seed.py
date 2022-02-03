from email.mime import image
from models import User


def seed_database(db):
    # Create all tables
    db.drop_all()
    db.create_all()

    # ensure no
    User.query.delete()

    brian = User(first_name="Brian",
                last_name="Aston")
    #imaginary friend one (could have been a pair partner ; ;)
    friend_one = User(first_name="Friend",
                    last_name="One")

    #imaginary friend two
    friend_two = User(first_name="Friend",
                    last_name="Two")

    # Add users
    db.session.add(brian)
    db.session.add(friend_one)
    db.session.add(friend_two)

    # commit transaction
    db.session.commit()
