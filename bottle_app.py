#! /usr/bin/env python3

import sqlite3
from bottle import *

# Database connections
database = sqlite3.connect('messenger.db')
cursor = database.cursor()


@route('/')
@route('/messenger')
@route('/messenger/login')
def messenger_login():
    """Index for Messenger."""
    return template('messenger')


@post('/messenger/login')
def login():
    """Logs in the user and handles registering a new account."""

    # Get login form data
    username = request.forms.get('username')
    password = request.forms.get('password')
    register = request.forms.get('register')

    # Handle if user clicked register
    if register == 'Register':
        # Check if username is taken
        if account_exists(username):
            return 'Username already taken'
        # Limit length of username and password
        if len(username) > 30:
            return 'Username cannot be more than 30 characters.'
        if len(password) > 30:
            return 'Password cannot be more than 30 characters.'
        # Everything's good. Create account
        generate_new_account(username, password)

    # Handle login. Check if account doesn't exist
    if not account_exists(username):
        return 'Account does not exist'

    # Check password
    if not validate_password(username, password):
        return 'Incorrect password'

    # Put the user's id and username into cookies
    token = get_user_id(username)
    response.set_cookie('token', token, secret=get_secret())
    # Send user to their dashboard
    redirect('/messenger/dashboard')


@route('/messenger/dashboard')
def dashboard():
    """Returns the user's dashboard."""
    # Get token cookie
    token = get_token()
    # Get username from get_token
    username = get_username(token)

    # Get a list of groups the user is in, and list of users that have send
    # you messages
    groups = get_user_groups(username)
    messages = get_user_messages(username)

    return template('dashboard', username=username,
                    messages=messages, groups=groups)


@post('/messenger/send')
def send():
    """Gathers form data and sends a message."""

    # Get form data
    message = request.forms.get('message')
    recipient = request.forms.get('recipient')
    # Get sender's username
    from_id = get_token()

    # Check if the receiving account exists
    if not account_exists(recipient):
        return 'That account does not exist'

    # Get receiver's id
    to_id = get_user_id(recipient)

    # Send message
    send_message(from_id, to_id, message)
    redirect('/messenger/dashboard')


@route('/messenger/read/<name>')
def read(name):
    """Returns a page listing all messages send by name."""
    # Check if account exists
    if not account_exists(name):
        return 'That account does not exist.'

    # Get ids for sender and receiver
    uid = get_token()
    from_id = get_user_id(name)

    # Get list of messasges sent
    messages = get_messages(from_id, uid)

    return template('read', messages=messages, sender=name)


@post('/messenger/reply/<name>')
def reply(name):
    """Gets reply form and sends the message"""
    # Check if account group_exists
    if not account_exists(name):
        return 'That account does not exist'

    # Get form data
    message = request.forms.get('message')

    # Get sender and receiver ids
    from_id = get_token()
    to_id = get_user_id(name)

    # Send the message
    send_message(from_id, to_id, message)
    redirect('/messenger/read/{}'.format(name))


@post('/messenger/groupreply/<name>')
def group_reply(name):
    """Gets form to reply to a group message."""

    # Get form data
    message = request.forms.get('message')

    # Get ids for user and group
    uid = get_token()

    # Check if group exists
    if not group_exists(name):
        return 'That group does not exist'

    group_id = get_group_id(name)

    # Send message
    send_group_message(uid, group_id, message)
    redirect('/messenger/group/{}'.format(name))


@post('/messenger/groupadd/<group>')
def group_add(group):
    """Adds a user to a group."""

    # Get form data
    name = request.forms.get('name')

    # Check if group doesn't exist
    if not group_exists(group):
        return 'Group does not exist'

    # Check for if account doesn't exist.
    if not account_exists(name):
        return 'That user does not exist'

    group_id = get_group_id(group)
    uid = get_user_id(name)

    # Check if user is already in the group.
    if user_in_group(uid, group_id):
        redirect('/messenger/group/{}'.format(group))

    # Add the user to the group
    add_to_group(uid, group_id)
    redirect('/messenger/group/{}'.format(group))


@post('/messenger/group/create')
def create_group():
    """Creates a new group from the form input."""

    # Get form data and user id
    group_name = request.forms.get('groupname')
    uid = get_token()

    # Check if group exists
    if group_exists(group_name):
        return 'Group already exists'

    # Generate the group
    generate_new_group(group_name, uid)
    redirect('/messenger/dashboard')


@route('/messenger/group/<name>')
def group(name):
    """Returns the group message page."""

    # Check if group exists
    if not group_exists(name):
        return 'Group does not exist'
    # Get user id and group id
    uid = get_token()
    group_id = get_group_id(name)

    # Check if user is in group
    if not user_in_group(uid, group_id):
        return 'You are not in this group'

    # Get group messages for the group
    messages = get_group_messages(group_id)
    return template('group', messages=messages, group_name=name)


@route('/messenger/admin')
@route('/messenger/admin/login')
def admin_accounts():
    """Returns the admin login page."""
    return template('admin_login')


@post('/messenger/admin/login')
def admin_accounts_post():
    """Receives the password form and verifies password."""
    # Get password from the form
    password = request.forms.get('password')

    # Validate
    if password != get_secret():
        return 'Incorrect password'

    # Set a token for the admin
    token = get_secret()
    response.set_cookie('admin', token, secret=get_secret())
    return template('admin')


@route('/messenger/admin/accounts')
def admin_accounts():
    """Returns a page of all accounts."""
    # Get admin cookie
    admin_cookie = request.get_cookie('admin', secret=get_secret())

    # Validate the cookie
    if not admin_cookie or admin_cookie != get_secret():
        redirect('/messenger/admin/login')

    # Select all accounts
    accounts = get_all_accounts()

    # Template will format the query into a table.
    return template('admin_accounts', accounts=accounts)


@route('/messenger/admin/messages')
def admin_message():
    """Returns a page of all messages."""
    # Get admin cookie
    admin_cookie = request.get_cookie('admin', secret=get_secret())

    # Validate the cookie
    if not admin_cookie or admin_cookie != get_secret():
        redirect('/messenger/admin/login')

    # Select all messages
    messages = get_all_messages()


    return template('admin_messages', messages=messages)


def get_token():
    """Returns the value inside the current token."""

    token = request.get_cookie('token', secret=get_secret())
    if not token:
        redirect('/messenger/login')

    return token


def send_message(from_account_id, to_account_id, message):
    """Adds a message to the database."""
    sql = """insert into Messages (fromAccountID, toAccountID, message)
             values (?, ?, ?)"""
    cursor.execute(sql, (from_account_id, to_account_id, message))
    database.commit()


def get_messages(from_account_id, to_account_id):
    """Returns all the messages/timestamps sent from one user to another."""

    sql = """select Accounts.username, message, time_sent from Messages
             join Accounts on Accounts.id = Messages.fromAccountID
             where (fromAccountID = ? and toAccountID = ?) or
                   (fromAccountID = ? and toAccountID = ?)"""
    cursor.execute(sql, (from_account_id, to_account_id,
                        to_account_id, from_account_id))

    messages = []

    for message in cursor:
        messages.append(message)

    return messages


def get_user_messages(username):
    """Returns list of names that username has messages from."""

    sql = 'select FromUsername from MessagesView where ToUsername = ?'
    cursor.execute(sql, (username, ))

    users = []

    for name in cursor:
        users.append(name[0])  # Pulls only the name

    return list(set(users))  # Removes duplicates


def account_exists(username):
    """Returns true if the account exists in the database."""

    sql = 'select * from Accounts where username = ?'
    cursor.execute(sql, (username, ))

    result = cursor.fetchone()

    # Check query for no result.
    if not result:
        return False

    return True


def validate_password(username, password):
    """Checks the database for the correct password.
    Throws exception when account does not exist."""

    sql = 'select password from Accounts where username = ?'
    cursor.execute(sql, (username, ))

    result = cursor.fetchone()

    # Check if query returned nothing
    if not result:
        raise RuntimeError('Password validator found no password for username')

    # Validate password
    if result[0] != password:
        return False

    return True


def get_username(id):
    """Return the username for a specific id."""

    sql = 'select username from Accounts where id = ?'
    cursor.execute(sql, (id,))

    result = cursor.fetchone()

    if not result:
        raise RuntimeError('User does not exist')

    return result[0]


def get_user_id(username):
    """Gets a user's id from the database.
    Throws exception when account does not exist."""

    sql = 'select id from Accounts where username = ?'
    cursor.execute(sql, (username, ))

    result = cursor.fetchone()

    # Check if query returned nothing.
    if not result:
        raise RuntimeError('Couldn\'t find user id')

    return result[0]


def generate_new_account(username, password):
    """Inserts the username and password into the database."""

    sql = 'insert into Accounts(username, password) values (?, ?)'
    cursor.execute(sql, (username, password))
    database.commit()


def group_exists(name):
    """Checks if a group with the same name already exists."""

    sql = 'select id from Groups where name = ?'
    cursor.execute(sql, (name, ))

    result = cursor.fetchone()

    if result:
        return True

    return False


def send_group_message(from_account_id, to_group_id, message):
    """Adds a group message to the database."""

    sql = """insert into GroupMessages (fromAccountID, toGroupID, message)
             values (?, ?, ?)"""
    cursor.execute(sql, (from_account_id, to_group_id, message))
    database.commit()


def generate_new_group(name, creator):
    """Creates a new group entry in the database and adds creator
       account to it."""

    sql = 'insert into Groups (name) values (?)'
    cursor.execute(sql, (name, ))
    database.commit()

    # Add the user that created the group to the group
    group_id = get_group_id(name)
    add_to_group(creator, group_id)


def get_group_id(name):
    """Returns id for a group."""

    sql = 'select id from Groups where name = ?'
    cursor.execute(sql, (name, ))

    result = cursor.fetchone()
    return result[0]


def get_user_groups(username):
    """Checks database and returns a list of all group names the user
       is apart of."""

    uid = get_user_id(username)
    sql = """select Groups.name from GroupMembers
             join Groups on Groups.id = GroupMembers.groupID
             where GroupMembers.accountID = ?"""
    cursor.execute(sql, (uid, ))

    groups = []

    for group_name in cursor:
        groups.append(group_name[0])

    # Returns only unique entrys
    return list(set(groups))


def add_to_group(account_id, group_id):
    """Adds a user to a group."""

    sql = 'insert into GroupMembers (accountID, groupID) values (?, ?)'
    cursor.execute(sql, (account_id, group_id))
    database.commit()


def user_in_group(account_id, group_id):
    """Returns if a user is in a particular group."""

    sql = 'select id from GroupMembers where accountID = ? and groupID = ?'
    cursor.execute(sql, (account_id, group_id))

    result = cursor.fetchone()

    # If the query returns something, then the user is in the group.
    if result:
        return True

    return False


def get_group_messages(group_id):
    """Return all the messages in a group chat."""

    sql = """select Accounts.username, message from GroupMessages
             join Accounts on Accounts.id = GroupMessages.fromAccountID
             where toGroupID = ?"""
    cursor.execute(sql, (group_id, ))

    messages = []

    for message in cursor:
        messages.append(message)

    return messages


def get_all_accounts():
    """Returns a list of all accounts in the database."""

    sql = 'select * from Accounts'
    cursor.execute(sql)

    accounts = []

    for account in cursor:
        accounts.append(account)

    return accounts


def get_all_messages():
    """Returns list of all direct messages in the database."""

    sql = 'select * from MessagesView'
    cursor.execute(sql)

    messages = []

    for message in cursor:
        messages.append(message)

    return messages


def get_secret():
    """Reads password from file secret."""
    with open('secret', 'r') as secret:
        return str(secret.readline())


if __name__ == '__main__':
    run(reloader=True)


application = default_app()
