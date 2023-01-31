import sqlite3
import asyncio

database = sqlite3.connect('server.db')
cursor = database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users('
               'user_id INT,'
               'name TEXT,'
               'gender TEXT,'
               'want_to_find TEXT,'
               'age INTEGER,'
               'faculty TEXT,'
               'photo TEXT,'
               'about TEXT,'
               'email TEXT,'
               'viewed_users TEXT,'
               'is_active INT'
               ')')
database.commit()


async def add_user(user_id, name, gender, want_to_find, age, faculty, photo, about, email):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()
    cursor.execute(
        'INSERT INTO users (user_id, name, gender, want_to_find, age, '
        'faculty, photo, about, email, viewed_users, is_active) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, "", 1)',
        (user_id, name, gender, want_to_find, age, faculty, photo, about, email))
    database.commit()


async def get_next_person(user_id):
    database = sqlite3.connect('server.db')
    cursor = database.cursor()

    # Get every id of active users
    cursor.execute('SELECT user_id FROM users WHERE is_active == 1 AND user_id != (?)', (user_id,))
    all_users = set([x[0] for x in cursor.fetchall()])
    if not all_users:
        return False
    cursor.execute('SELECT viewed_users FROM users WHERE user_id == (?)', (user_id,))
    result = cursor.fetchall()
    # If no one is viewed
    if not result:
        next_id = list(all_users)[0]
        new_viewed_list = [next_id]

    else:
        viewed_set = str(result[0][0]).split(',')
        viewed_set = set(map(int, viewed_set))

        not_viewed_users = all_users.difference(viewed_set)
        print(viewed_set)
        print(not_viewed_users)
        # Get random user if everyone is viewed
        if len(not_viewed_users) == 0:
            next_id = list(all_users)[0]
            new_viewed_list = [next_id]
        else:
            next_id = list(not_viewed_users)[0]
            new_viewed_list = list(viewed_set) + [next_id]

    new_viewed = ','.join(list(map(str, new_viewed_list)))
    cursor.execute('UPDATE users SET viewed_users = (?) WHERE user_id = (?)', (new_viewed, user_id))
    database.commit()

    cursor.execute('SELECT user_id, name, age, faculty, photo, about FROM users WHERE user_id = (?)', (next_id,))
    next_user = cursor.fetchall()
    return next_user


async def test(user_id):
    print(await get_next_person(user_id))

# check

asyncio.run(test(11111))
