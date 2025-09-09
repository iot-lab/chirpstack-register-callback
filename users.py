"""
    Manage users for ChirpStack LNS thanks to the ChirpStack API
"""

from chirpstack_api import api

import auth_token as config


def get_nb_users(channel):
    """ Get number of registred users """
    client = api.UserServiceStub(channel)
    req = api.ListUsersRequest()
    resp = client.List(req, metadata=config.AUTH_TOKEN)
    nb_users = resp.total_count
    return nb_users

def get_list_users(channel):
    """ Get list of registered users """
    client = api.UserServiceStub(channel)
    nb_users = get_nb_users(channel)
    i = 0
    results = []
    while i < nb_users:
        req = api.ListUsersRequest()
        req.limit = 10
        req.offset = i
        resp = client.List(req, metadata=config.AUTH_TOKEN)
        for j in resp.result:
            results.append(j)
        i += 10
    return results

def print_list_users(users):
    """ List all users """
    for k in users:
        print(k.id, k.email, k.is_admin)

def create_user(channel, email, password=None):
    """ Create a new user """
    client = api.UserServiceStub(channel)
    req = api.CreateUserRequest()
    req.user.email = email
    if password is not None:
        req.password = password
    req.user.is_active = True
    resp = client.Create(req, metadata=config.AUTH_TOKEN)
    print(resp)
    return resp.id

def get_user_id(channel, email):
    """ Get user ID by email (email in v3) """
    user_id = "-1"
    users = get_list_users(channel)
    for user in users:
        if user.email == email:
            user_id = user.id
    return user_id

def delete_user_by_id(channel, user_id):
    """ Delete user by ID """
    client = api.UserServiceStub(channel)
    req = api.DeleteUserRequest()
    req.id = user_id
    resp = client.Delete(req, metadata=config.AUTH_TOKEN)
    print(resp)
    return resp
