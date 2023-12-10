import sys

from sql.database import SessionLocal
from sql.models import User
from api.authorization.utils import get_password_hash


def create_user():
    username = input('Insert username: ')
    password = input('Insert password: ')
    password_confirm = input('Repeat password:')
    if password != password_confirm:
        print('passwords aren\'t matched, please try again')
    push_user_to_db(username, password)
    print('user has been created!')


def push_user_to_db(username, password):
    session = SessionLocal()
    try:
        hashed_password = get_password_hash(password)
        session.add(User(username=username, hashed_password=hashed_password))
        session.commit()
    finally:
        session.close()

commands = {
    'create_user': create_user
}

if __name__ == '__main__':
    command = sys.argv[-1]

    if command not in commands:
        raise ValueError('Uknown command')

    commands[command]()
