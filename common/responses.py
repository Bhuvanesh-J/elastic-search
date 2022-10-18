from flask import jsonify


def success(content, message=None):
    res = {}
    res['content'] = content
    resp = {}
    resp['status'] = 200
    resp['message'] = 'Successfully created'
    if message:
        resp['message'] = message
    res['response'] = resp
    response = jsonify(res)
    response.status_code = 200
    response.content_type = "application/json"
    return response


def failed(content, message=None):
    res = {}
    res['content'] = content
    resp = {}
    resp['status'] = 400
    resp['message'] = 'Failed to create'
    if message:
        resp['message'] = message
    res['response'] = resp
    response = jsonify(res)
    response.status_code = 400
    response.content_type = "application/json"
    return response
