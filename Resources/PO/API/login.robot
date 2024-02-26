*** Settings ***
Documentation    https://sospublicapi.docs.apiary.io/#reference/login/login
Library  BuiltIn
Library  Collections
Library  OperatingSystem
Library  RequestsLibrary
Library  ../../../Libraries/jsonlib.py
Library  JSONSchemaLibrary      ${EXECDIR}/Resources/PO/API/schemas
Library  ../../../Libraries/BColors.py
Library  pabot.PabotLib


*** Keywords ***
I Update Json /login
    [Arguments]  ${email_address}  ${password}
    Acquire Lock                    login.json
    Update Json Login               ${EXECDIR}${path_to_json}[login]        username    ${email_address}
    Update Json Login               ${EXECDIR}${path_to_json}[login]        password    ${password}
    Release Lock                    login.json

Post Request /login
    ${request_body}                 Get Binary File             ${EXECDIR}${path_to_json}[login]
    Log                             ${request_body}
    ${response}                     Post On Session              sos_api
    ...                             ${api_endpoints}[login]
    ...                             headers=${headers_no_auth}
    ...                             data=${request_body}
    Should Be Equal As Strings      ${response.status_code}      200
    ${response_body_json}           Set Variable        ${response.json()}
    Log                             ${response_body_json}
    # Clean values for username, password objects:
    Acquire Lock                    login.json
    Update Json Login               ${EXECDIR}${path_to_json}[login]        username        user_email@mail.com
    Update Json Login               ${EXECDIR}${path_to_json}[login]        password        user_pass
    Release Lock                    login.json
# Check main attributes:
    # Assert the lenght:
    Length Should Be                ${response_body_json}                   2
    Length Should Be                ${response_body_json['data']}           4
    # Assert the values:
    Should Be Equal As Strings      ${response_body_json['data']['type']}   token
    Set Suite Variable              ${AUTH_TOKEN}  ${response_body_json['data']['token']}
    Set Suite Variable              ${AUTH_SECRET}  ${response_body_json['data']['secret']}
