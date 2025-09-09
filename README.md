# ChirpStack Register Callback

Web service based on ChirpStack API to automatically provision user and tenant.
The service handles request for registration callback a ChirpStack instance
configured with openid user authentication (user_authentication.openid_connect).

## Configure

Edit config.ini file. Change `server` with your ChirpStack instance. In order to
get your `api_token`, login as global admin and go to Network Server / API keys
and click to `Add API key` :

```
[log]
# Debug level, could be INFO or DEBUG
level = DEBUG

[flask]
port = 8085

[chirpstack]
# ChirpStack LNS instance with API server
server = chirpstack.example.com:443
# uncomment server_cn to override server name in ssl cert, usefull with docker container in same private network
# server_cn = lns.example.com
# Global admin token 
api_token = ChangeMe
```

## Install and run

Setup Python environnement: 

```
virtualenv ~/python-env/chirpstack-register-callback
source ~/python-env/chirpstack-register-callback/bin/active
pip install -r requirements.txt
```

Run:

```
python ./main.py
```

## Install and run with Docker

### Build image

* Build Docker image

```
docker build -t chirpstack-register-callback .
```

### Run

* Run in foreground

```
docker run --rm -it \
    -p 8085:8085 \
    --name chirpstack-register-callback \
    --volume $PWD/config.ini:/project/config.ini:ro \
    chirpstack-register-callback
```

* Run as a daemon in background and restart on failure or reboot unless if manually stop with docker

```
docker run  -rm -it \
    -p 8085:8085 \
    --restart unless-stopped -d \
    --name chirpstack-register-callback \
    --volume $PWD/config.ini:/project/config.ini:ro \
    chirpstack-register-callback
```

##  Testing with Curl Command

Test if services is reachable

```
curl -ks http://127.0.0.1:8085/hello
```

Test to register with command line parameters
```
curl -ks --header "Content-Type: application/json" --request POST --data '{"preferred_username":"toto","email":"toto@toto.com"}' http://127.0.0.1:8085/register
```

Test to register with data file parameters

```
curl -ks --header "Content-Type: application/json" --request POST --data "@tests/data.json" http://127.0.0.1:8085/register
```