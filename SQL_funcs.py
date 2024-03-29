import sqlite3
import random

database = sqlite3.connect('server.db')
cursor = database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users('
               'user_id INT,'
               'name TEXT,'
               'gender TEXT,'
               'want_to_find TEXT,'
               'age INTEGER,'
               'university TEXT,'
               'faculty TEXT,'
               'photo TEXT,'
               'about TEXT,'
               'viewed_users TEXT,'
               'is_active INT'
               ')')
database.commit()


def make_parsable(text: str):
    gaps = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for gap in gaps:
        text = text.replace(gap, f"\{gap}")
    print(text)
    return text


async def add_user(user_id, name, gender, want_to_find, age, faculty, university, photo,
                   about):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute(
        'INSERT INTO users (user_id, name, gender, want_to_find, age, '
        'faculty, university, photo, about, viewed_users, is_active) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, "", 1)',
        (
            user_id, make_parsable(name), gender, want_to_find, age, make_parsable(faculty), make_parsable(university),
            photo, make_parsable(about),
        ))
    database.commit()


async def get_next_person(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()

    # Get the gender user wants to find
    cursor.execute('SELECT want_to_find FROM users WHERE user_id = (?)',
                   (user_id,))
    gender_user_wants = cursor.fetchone()[0]

    # Get every id of active users that satisfies preferences
    cursor.execute(
        'SELECT user_id FROM users WHERE is_active == 1 AND user_id != (?) AND gender = (?)',
        (user_id, gender_user_wants))
    all_users = set([x[0] for x in cursor.fetchall()])
    # Return False if no users are available
    if not all_users:
        return False

    # Get viewed users
    cursor.execute('SELECT viewed_users FROM users WHERE user_id == (?)',
                   (user_id,))
    result = cursor.fetchall()
    # If no one is viewed
    if result == [('',)]:
        next_id = list(all_users)[0]
        new_viewed_list = [next_id]

    else:

        viewed_set = str(result[0][0]).split(',')
        viewed_set = set(map(int, viewed_set))

        not_viewed_users = all_users.difference(viewed_set)
        # Get random user if everyone is viewed
        if len(not_viewed_users) == 0:
            next_id = list(all_users)[random.randint(0, len(all_users)-1)]
            new_viewed_list = [next_id]
        else:
            next_id = list(not_viewed_users)[random.randint(0, len(not_viewed_users)-1)]
            new_viewed_list = list(viewed_set) + [next_id]

    new_viewed = ','.join(list(map(str, new_viewed_list)))
    cursor.execute('UPDATE users SET viewed_users = (?) WHERE user_id = (?)',
                   (new_viewed, user_id))
    database.commit()

    cursor.execute(
        'SELECT user_id, name, age, faculty, university, photo, about FROM users WHERE user_id = (?)',
        (next_id,))
    next_user = cursor.fetchone()
    return next_user


async def get_user_data(user_id):
    user_id = int(user_id)
    database = sqlite3.connect('server.db')
    cursor = database.cursor()

    cursor.execute(
        'SELECT user_id, name, age, faculty, university, photo, about FROM users WHERE user_id = (?)',
        (user_id,))
    result = cursor.fetchone()
    if not result:
        return None
    return result


async def get_active_status(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute('SELECT is_active FROM users WHERE user_id = (?)',
                   (user_id,))
    result = cursor.fetchone()
    return result


async def get_all_user_data(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()

    cursor.execute(
        'SELECT user_id, name, age, faculty, university, photo, about FROM users '
        'WHERE user_id = (?)',
        (user_id,))
    result = cursor.fetchone()
    if not result:
        return None
    return result


async def update_user_data(user_id, data):
    name, gender, want_to_find, age, faculty, university, photo, about = data
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute(
        'UPDATE users SET name = (?), gender=(?), want_to_find=(?), age= (?), faculty= (?), university = (?), '
        'photo= (?), about= (?)'
        ' WHERE user_id = (?)',
        (make_parsable(name), gender, want_to_find, age, make_parsable(faculty), make_parsable(university), photo,
         make_parsable(about), user_id))
    database.commit()


async def update_user_about(user_id, about):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute('UPDATE users SET about= (?) WHERE user_id = (?)',
                   (make_parsable(about), user_id))
    database.commit()


async def delete_user(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()

    cursor.execute('DELETE FROM users WHERE user_id = (?)', (user_id,))
    database.commit()


async def deactivate_profile(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute('UPDATE users SET is_active= 0 WHERE user_id = (?)',
                   (user_id,))
    database.commit()


async def activate_profile(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute('SELECT is_active FROM users WHERE user_id = (?)', (user_id,))
    is_active = cursor.fetchone()
    print(is_active)
    if is_active[0] == 0:
        cursor.execute('UPDATE users SET is_active= 1 WHERE user_id = (?)',
                       (user_id,))
        database.commit()


async def get_all_users():
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute('SELECT user_id FROM users')
    user_list = list(map(lambda x: x[0], cursor.fetchall()))
    return user_list


async def test(user_id):
    print(await get_next_person(user_id))
