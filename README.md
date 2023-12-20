MongoDB WebApp Sample
=====================

This is a simple web application written in Python meant to showcase MongoDB,
with a focus on Canonical's Charmed MongoDB solution.

Installation
------------

We highly recommend using a Python virtual env to avoid conflicting
dependencies:

```
sudo apt-get install python3-pip python3-venv -y
python3 -m venv create sample_venv
. ./sample_venv/bin/activate
```

The sample application can then be installed like so:

```
pip install git+https://github.com/petrutlucian94/mongo-webapp-sample
```

Running
=======

Use ``mongo-webapp-sample-api`` to launch the application.

```
MONGO_CREDS="mongoAdmin:P%40ssw0rd"
MONGO_HOST="mongo-snap.multipass:27017"
export SAMPLEAPP_MONGO_URL="mongodb://${MONGO_CREDS}@${MONGO_HOST}/"

mongo-webapp-sample-api
```

A few settings can be provided through environment variables:

* ``SAMPLEAPP_MONGO_URL``
  * the URL used to establish MongoDB connections, can also include credentials.
  * default: ``mongodb://localhost:27017/``
* ``SAMPLEAPP_MONGO_DB_NAME``
  * the name of the database used to store data
  * default: ``sample_app``
* ``SAMPLEAPP_DEBUG``
  * set to ``True`` to enable debug logging
  * default: ``False``
* ``SAMPLEAPP_MONGO_CONN_TIMEOUT``
  * database connection timeout in seconds
  * default: 5
* ``SAMPLEAPP_MONGO_OP_TIMEOUT``
  * database operation timeout in seconds
  * default: 10

Gunicorn can be used for a more production-like environment:

```
pip install gunicorn

gunicorn -b 0.0.0.0:5000 -w 4 'mongo_webapp_sample.cmd.api:register_app()'
```

Usage
-----

Sorry, no GUI or CLI client. Feel free to use cURL.

Create a few stores
===================

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"Los Pollos Hermanos", "description": "Los Pollos Hermanos, where something delicious is always cooking.", "location": {"coordinates": [-106.668038, 35.1247337]}, "tags": ["restaurant", "food"]}' \
  http://localhost:5000/stores

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"Ollivanders Wand Shop", "description": "Fine Wands since 382 BC", "location": {"coordinates": [21.2228283, 45.743279]}}' \
  http://localhost:5000/stores

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"Wonkas Chocolate Factory", "description": "This little piece of gum is a three-course dinner.", "location": {"coordinates": [21.2470794, 45.7536246]}}' \
  http://localhost:5000/stores

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"Mos Eisley Cantina", "description": "Tentacles, claws and hands... wrapped around drinking utensils.", "location": {"coordinates": [21.2399956, 45.7484419]}, "tags": ["restaurant", "food", "drinks"], "address": "Mos Eisley, Tatooine"}' \
  http://localhost:5000/stores
```

List stores
===========

```
# list all stores
curl http://localhost:5000/stores

# list stores in a 5km radius from a given location
curl "http://localhost:5000/stores?near=21.2283754,45.74102&max_distance=5000"  | json_pp

# text search
curl "http://localhost:5000/stores?text=wands"  | json_pp

# text search
curl "http://localhost:5000/stores?text=restaurant"  | json_pp
```

Update store
============

```
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"address": "Albuquerque, New Mexico"}' \
  http://localhost:5000/stores/44135c4c-e569-4e6f-9677-cead47c108f3
```

Retrieve store
==============

```
curl http://localhost:5000/stores/44135c4c-e569-4e6f-9677-cead47c108f3
```

Delete store
============

```
curl --request DELETE \
  http://localhost:5000/stores/44135c4c-e569-4e6f-9677-cead47c108f3
```

Running the tests
-----------------

This project has a few functional tests that can be invoked using tox:

```
sudo apt-get install -y tox

MONGO_CREDS="mongoAdmin:P%40ssw0rd"
MONGO_HOST="mongo-snap.multipass:27017"
export SAMPLEAPP_MONGO_URL="mongodb://${MONGO_CREDS}@${MONGO_HOST}/"

tox

```