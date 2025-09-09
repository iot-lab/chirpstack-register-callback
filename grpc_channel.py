"""
    Manage Grpc connexion with Chirpstack API
"""

import grpc
import certifi


def grpc_channel_create(server, cert_cn=None):
    """ Create secure Grpc channel with API server over HTTPS """
    cacert_path = certifi.where()
    with open(cacert_path, 'rb') as f:
        certificate_chain = f.read()
    creds = grpc.ssl_channel_credentials(root_certificates=certificate_chain)
    if cert_cn is not None:
        options = (('grpc.ssl_target_name_override', cert_cn,),)
        channel = grpc.secure_channel(server, creds, options)
    else:
        channel = grpc.secure_channel(server, creds)
    return channel
