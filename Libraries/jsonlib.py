import json
import urllib3
import hashlib
import hmac
from urllib.parse import quote

urllib3.disable_warnings()

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
USER_AGENT = 'SOS.ApiRequestTask/1.0'
CONTENT_TYPE = 'application/vnd.api+json'


def load_json_file(js_file):
    json_file = open(js_file, "r")
    parsed_data = json.load(json_file)
    json_file.close()
    return parsed_data


def write_and_close_json(js_file, parsed_data):
    json_file = open(js_file, "w+")
    json_file.write(json.dumps(parsed_data))
    json_file.close()


def update_json_login(js_file, attribute, new_value):
    parsed_data = load_json_file(js_file)
    parsed_data["data"]["attributes"][attribute] = new_value
    write_and_close_json(js_file, parsed_data)


def auth_sigv1(auth_token, auth_secret, request_body):
    """
    This function should be used only for requests that require a request body (e.g. POST, PATCH, etc.).
    There are a few options to get 'Signature' hash:
    Option 1:
            signature = hmac.new(auth_secret.encode(), request_body.encode(), hashlib.sha256).hexdigest()
    Option 2:
            signature = hmac.new(digestmod=hashlib.sha256, msg=request_body.encode(), key=auth_secret.encode()).hexdigest()
    Option 3:
            params = {
                'digestmod': hashlib.sha256,
                'msg': request_body.encode(),
                'key': auth_secret.encode(),
            }
            signature = hmac.new(**params).hexdigest()
    """

    signature = hmac.new(auth_secret.encode(), request_body, hashlib.sha256).hexdigest()

    headers_auth = {
        "User-Agent": USER_AGENT,
        "Content-Type": CONTENT_TYPE,
        "Accept": CONTENT_TYPE,
        "Authorization": f"SOS-SIGV1 {auth_token};{signature}"
    }
    return headers_auth


def auth_sigv1_no_body(auth_token, auth_secret):
    """
    This function should be used only for requests that don't require a request body (e.g. GET requests).

    There are a few options to get 'Signature' hash:
    Option 1:
            signature = hmac.new(auth_secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    Option 2:
            signature = hmac.new(digestmod=hashlib.sha256, msg=body.encode(), key=auth_secret.encode()).hexdigest()
    Option 3:
            params = {
                'digestmod': hashlib.sha256,
                'msg': body.encode(),
                'key': auth_secret.encode(),
            }
            signature = hmac.new(**params).hexdigest()
    """

    body = ""

    params = {
        'digestmod': hashlib.sha256,
        'msg': body.encode(),
        'key': auth_secret.encode(),
    }
    signature = hmac.new(**params).hexdigest()

    headers_auth = {
        "User-Agent": USER_AGENT,
        "Content-Type": CONTENT_TYPE,
        "Accept": CONTENT_TYPE,
        "Authorization": f"SOS-SIGV1 {auth_token};{signature}"
    }
    return headers_auth


def auth_sos_noid(auth_token):
    headers_auth = {
        "User-Agent": USER_AGENT,
        "Content-Type": CONTENT_TYPE,
        "Accept": CONTENT_TYPE,
        "Authorization": f"SOS-NOID {auth_token}"
    }
    return headers_auth


def create_endpoint():
    api_endpoints = {
        "login": "/login",
        "me": "/me"
    }
    return api_endpoints


def update_json(js_file, data):
    json_file = open(js_file, "w+")
    json_file.write(json.dumps(data))
    json_file.close()


def requote_email(email):
    return quote(email.encode("utf-8"))
