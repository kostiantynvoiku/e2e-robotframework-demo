*** Settings ***
Documentation    https://sospublicapi.docs.apiary.io/#reference/users/current-user
Library  Collections
Library  OperatingSystem
Library  RequestsLibrary
Library  ../../../Libraries/jsonlib.py
Library  JSONSchemaLibrary      ${EXECDIR}/Resources/PO/API/schemas
Library  ../../../Libraries/BColors.py


*** Keywords ***
Send Request GET ME
    ${headers_auth}                 Auth Sigv1 No Body                                                                  ${AUTH_TOKEN}  ${AUTH_SECRET}
    ${response}                     Get On Session                                                                      sos_api
    ...                             ${API_ENDPOINTS}[me]
    ...                             headers=${headers_auth}
    Should Be Equal As Strings      ${response.status_code}                                                             200
    Log To Console Blue             INFO: Send API request:  GET /me == ${response.status_code}
    Set Test Variable               ${response_body_json}                                                               ${response.json()}
    Log                             ${response_body_json}
    RETURN                          ${response_body_json}

Assert Data Is Correct
    Should Be Equal As Strings      ${response_body_json['data']['type']}                                               user
    Should Be Equal As Strings      ${response_body_json['data']['attributes']['country_code']}                         ${COUNTRY_CODE}
    Should Be Equal As Strings      ${response_body_json['data']['attributes']['first_name']}                           ${CUSTOMER_FIRST_NAME}
    Should Be Equal As Strings      ${response_body_json['data']['attributes']['last_name']}                            ${CUSTOMER_LAST_NAME}
    Should Be Equal As Strings      ${response_body_json['data']['attributes']['full_name']}                            ${CUSTOMER_FIRST_NAME} ${CUSTOMER_LAST_NAME}
