"""
    Manage tenants for ChirpStack LNS thanks to the ChirpStack API
"""

from chirpstack_api import api

import auth_token as config


OFFSET = 10

def get_nb_tenants(channel):
    """ Get number of registered tenant """
    client = api.TenantServiceStub(channel)
    req = api.ListTenantsRequest()
    resp = client.List(req, metadata=config.AUTH_TOKEN)
    nb_orgs = resp.total_count
    return nb_orgs

def get_nb_org_users(channel, org_id):
    """ Get number of Users for an tenant """
    client = api.TenantServiceStub(channel)
    req = api.ListTenantUsersRequest()
    req.tenant_id = org_id
    resp = client.ListUsers(req, metadata=config.AUTH_TOKEN)
    nb_users = resp.total_count
    return nb_users

def get_list_tenants(channel):
    """
        Get all tenants from server.
        Return a list for tenants.
    """
    client = api.TenantServiceStub(channel)
    nb_orgs = get_nb_tenants(channel)
    i = 0
    results = []
    while i < nb_orgs:
        req = api.ListTenantsRequest()
        req.limit = OFFSET
        req.offset = i
        resp = client.List(req, metadata=config.AUTH_TOKEN)
        for j in resp.result:
            results.append(j)
        i += OFFSET
    return results

def get_org_users(channel, org_id):
    """ Get number of associated users for an tenant """
    client = api.TenantServiceStub(channel)
    nb_users = get_nb_org_users(channel, org_id)
    i = 0
    results = []
    while i < nb_users:
        req = api.ListTenantUsersRequest()
        req.tenant_id = org_id
        req.limit = OFFSET
        req.offset = i
        resp = client.ListUsers(req, metadata=config.AUTH_TOKEN)
        for j in resp.result:
            results.append(j)
        i += OFFSET
    return results

def print_list_tenants(channel, orgs):
    """ List all tenants """
    for k in orgs:
        print(f"ORG {k.id} {k.name}")
        nb_users = get_nb_org_users(channel, k.id)
        print(f"   NBUSERS: {nb_users}")
        users = get_org_users(channel, k.id)
        for u in users:
            print("       " + u.email)

def create_tenant(channel, name, can_have_gateways=False):
    """ Create a new organization """
    client = api.TenantServiceStub(channel)
    req = api.CreateTenantRequest()
    req.tenant.name = name
    req.tenant.can_have_gateways = can_have_gateways
    resp = client.Create(req, metadata=config.AUTH_TOKEN)
    print(resp)
    return resp.id

def add_user_tenant(channel, organization_id, email):
    """ Add a user to an organization """
    client = api.TenantServiceStub(channel)
    req = api.AddTenantUserRequest()
    req.tenant_user.tenant_id = organization_id
    req.tenant_user.is_admin = True
    req.tenant_user.email = email
    resp = client.AddUser(req, metadata=config.AUTH_TOKEN)
    print(resp)

def get_tenant_id_by_name(channel, name):
    """ Get tenant ID by name """
    tenant_id = "-1"
    tenants = get_list_tenants(channel)
    for ten in tenants:
        if ten.name == name:
            tenant_id = ten.id
    return tenant_id

def delete_tenant_by_id(channel, tenant_id):
    """ Delete tenant by ID """
    client = api.TenantServiceStub(channel)
    req = api.DeleteTenantRequest()
    req.id = tenant_id
    resp = client.Delete(req, metadata=config.AUTH_TOKEN)
    return resp

def delete_tenant_by_name(channel, name):
    """ Delete tenant by name """
    tenant_id = get_tenant_id_by_name(channel, name)
    if tenant_id == "-1":
        print("Tenant not found")
    else:
        print("Deleting tenant id " + str(tenant_id))
        delete_tenant_by_id(channel, tenant_id)
