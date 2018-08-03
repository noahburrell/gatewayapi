#!/usr/bin/python
import common
import re
from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)


# Handle 404 errors
@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'Not authorized'}), 401)


# Handle 400 errors
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Malformed request'}), 400)


# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Handle device PSK lookups
@app.route('/api/v1.0/psk/<int:uid>/<string:psk>', methods=['GET'])
def get_device(uid, psk):
    if not request.headers.get('X-Auth-Token'):
        abort(401)
    if common.authenticate(uid, request.remote_addr, request.headers.get('X-Auth-Token')) is not True:
        abort(401)

    result = common.psk_lookup(uid, psk)
    if len(result) == 0:
        abort(404)
    return jsonify({'device': result[0]})


# Handle updating device MAC associated with PSK
@app.route('/api/v1.0/mac/<int:uid>/<int:id>', methods=['PUT'])
def update_mac(uid, id):
    if not request.headers.get('X-Auth-Token'):
        abort(401)
    if common.authenticate(uid, request.remote_addr, request.headers.get('X-Auth-Token')) is not True:
        abort(401)

    result = common.dev_lookup(uid, id)
    if len(result) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'mac_add' in request.json and type(request.json['mac_add']) is not unicode:
        abort(400)
    # Confirm a valid mac exists in the request using regex
    mac_parse = re.compile(ur'(?:[0-9a-fA-F]:?){12}')
    mac_list = re.findall(mac_parse, request.json['mac_add'])
    # If there is not exactly 1 mac address matched, abort
    if len(mac_list) is not 1:
        abort(400)

    return jsonify({"status": common.update_mac(id, mac_list[0])})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
