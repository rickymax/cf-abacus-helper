'''
    api.py

    Abacus Helper API

    @Author: rickylo@iii.org.tw
'''
import datetime
import json
import re
import os

from app import app
from serviceMgt import cf_login, cf_token, abacus_helper, asking_helper
from utils import runcmd

from flask import Flask, jsonify, redirect, request
from flasgger import Swagger


if 'VCAP_APPLICATION' in os.environ:
    cf_api_endpoint = os.getenv('CF_API_ENDPOINT')
    cf_user = os.getenv('CF_USER')
    cf_password = os.getenv('CF_PASSWORD')
    vcap = json.loads(os.getenv('VCAP_APPLICATION'))
    if 'application_uris' in vcap:
        uri = vcap['application_uris'][0]


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/demo/cf_login", methods=['GET'])
def demo_cf_login():
    """
    Demo
    Log into Cloud Foundry
    ---
    tags:
      - demo
    """
    ret = cf_login()
    return jsonify({'result': ret})

@app.route("/demo/cf_token", methods=['GET'])
def demo_cf_token():
    """
    Demo
    Retrieve OAuth token for the current Cloud Foundry session
    ---
    tags:
      - demo
    """
    ret = cf_token()
    return jsonify({'result': ret})

@app.route("/demo/helper", methods=['GET'])
def demo_update_helper():
    """
    Demo
    Update Abacus helper
    ---
    tags:
      - demo
    """
    ret = abacus_helper()
    return jsonify(ret)

@app.route("/v1/helper/<string:service_instance_id>", methods=['GET'])
def demo_helper(service_instance_id):
    """
    Demo
    Get help from Abacus helper
    ---
    tags:
      - demo
    parameters:
      - name: service_instance_id
        in: path
        type: string
        required: true
        description: servie instance guid
    """
    ret = asking_helper(service_instance_id)

    if ret is None:
        raise InvalidUsage('The service_instance_id is not exist', status_code=404)
    else:
        return jsonify(ret)

@app.route("/")
def hello():
    return redirect("http://{}/apidocs/index.html".format(uri), code=302)

