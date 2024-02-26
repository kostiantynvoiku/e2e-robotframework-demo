*** Settings ***
Documentation       API Keywords
Library             BuiltIn
Resource            ../Resources/PO/API/login.robot
Resource            ../Resources/PO/API/me.robot


*** Keywords ***
I Start HTTP Session
    Create Session                 sos_api                     ${START_URL}api.php

I Close All HTTP Sessions
    Delete All Sessions

I Login To API
    [Arguments]  ${email_address}  ${password}
    I Update Json /login  ${email_address}  ${password}
    Post Request /login

I Fetch Data With API
    [Teardown]   I Close All HTTP Sessions
    I Start HTTP Session
    I Login To API  ${CUSTOMER_EMAIL}  ${PASSWORD}
    Send Request GET ME

Verify Returned Data
    Assert Data Is Correct
