"""
    Flask web server to handle user registration for ChirpStack LNS
"""

import logging
import sys

from configparser import RawConfigParser

from flask import Flask
from flask import request

from grpc_channel import grpc_channel_create
from users import create_user, get_user_id
from tenants import get_tenant_id_by_name, create_tenant, add_user_tenant, get_org_users


# config values
CFG = RawConfigParser()
CFG.read('config.ini')

PORT = CFG.getint('flask', 'port', fallback=8085)

def setup_logger():
    """ Setup default logger """
    log_level = CFG.get('log', 'level')

    logging.basicConfig(
        level = log_level,
        format = '%(asctime)s.%(msecs)03d %(message)s',
        datefmt = '%Y-%m-%d,%H:%M:%S',
        stream = sys.stdout
    )
    _logger = logging.getLogger('chirpstack-lorawan-monitoring')
    return _logger

# Init logger
LOGGER = setup_logger()

app = Flask(__name__)

@app.route('/hello')
def hello():
    """ Simple hello world endpoint """
    return print_hello()

def print_hello():
    """ Simple hello world functinon """
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register():
    """ Handle user registration endpoint """
    LOGGER.debug("request method: %s", request.method)
    if request.method == 'POST':
        data = request.data
        handle_registration(data)
        return "Registered successfully!"
    return "Invalid request method", 405

def handle_registration(data):
    """ Handle user registration data """
    # Process the registration data
    LOGGER.info("Handling registration with data: %s", data)
    email = request.json.get('email')
    preferred_username = request.json.get('preferred_username')
    LOGGER.debug("email=%s preferred_username=%s", email, preferred_username,)


    LOGGER.info("Register process for user %s ...", email)
    server = CFG.get('chirpstack', 'server')
    if CFG.has_option('chirpstack', 'server_cn'):
        server_cn = CFG.get('chirpstack', 'server_cn')
        LOGGER.debug("Using server_cn %s to override ssl cert for %s", server_cn, server)
        channel = grpc_channel_create(server, cert_cn=server_cn)
    else:
        LOGGER.debug("Using default ssl cert for %s", server)
        channel = grpc_channel_create(server)

    LOGGER.debug("Test if user %s already exists...", email)
    user_id = get_user_id(channel, email)
    LOGGER.debug("user_id=%s for %s", user_id, email)
    if user_id != '-1':
        LOGGER.debug("User %s already exists", email)
    else:
        LOGGER.info("User %s does not exist, creating...", email)
        create_user(channel, email)

    LOGGER.debug("Test if tenant %s already exists", email)
    tenant_id = get_tenant_id_by_name(channel, email)
    LOGGER.debug("tenant_id=%s", tenant_id)
    if tenant_id != '-1':
        LOGGER.debug("Tenant %s already exists", email)
    else:
        LOGGER.info("Tenant does not exist, creating...")
        tenant_id = create_tenant(channel, email, can_have_gateways=True)

    LOGGER.debug("Test if user %s is assigned to tenant %s", email, email)
    # test if multiple users assigned to same tenant
    if len(get_org_users(channel, tenant_id)) > 0:
        if email in [u.email for u in get_org_users(channel, tenant_id)]:
            LOGGER.debug("User %s already assigned to tenant %s", email, email)
        else:
            LOGGER.info("User %s not assigned to tenant %s, assigning...", email, email)
            add_user_tenant(channel, tenant_id, email)
    else:
        LOGGER.info("User %s not assigned to tenant %s, assigning...", email, email)
        add_user_tenant(channel, tenant_id, email)
    LOGGER.info("Register process for user %s ... [DONE]", email)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
