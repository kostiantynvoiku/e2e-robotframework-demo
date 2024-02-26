from robot.libraries.BuiltIn import BuiltIn

user_uuid = BuiltIn().get_variable_value("${user_uuid}")

api_endpoints = {
    "login": "/login",
    "me": "/me"
}


headers_no_auth = {
    "User-Agent": "SOS.ApiRequestTask/1.0",
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json"
}


path_to_json = {
    "login": "/Resources/PO/API/data_body/login.json",
}


