*** Settings ***
Library  DateTime
Library  SeleniumLibrary
Library  ../../../Libraries/MimesisLibrary.py


*** Variables ***
${FIRST_NAME}                           //*[@data-cy="CI_userSignUp_firstName"]
${LAST_NAME}                            //*[@data-cy="CI_userSignUp_lastName"]
${EMAIL_ADDRESSS}                       //*[@data-cy="CI_userSignUp_email"]
${PASSWORD_FIELD}                       //*[@data-cy="CI_userSignUp_password"]
${SUBMIT}                               //*[@data-cy="CI_userSignUp_submit"]
${DASHBOARD_AVATAR}                     //*[@data-cy="CI_userDashboard_avatar"]


*** Keywords ***
Input User Names
    ${CUSTOMER_FIRST_NAME}              Generate Random First Name  ${LOCALE}
    ${CUSTOMER_LAST_NAME}               Generate Random Last Name   ${LOCALE}
    Set Suite Variable                  ${CUSTOMER_FIRST_NAME}
    Set Suite Variable                  ${CUSTOMER_LAST_NAME}
    Input Text                          ${FIRST_NAME}           ${CUSTOMER_FIRST_NAME}
    Input Text                          ${LAST_NAME}            ${CUSTOMER_LAST_NAME}

Input Email Address And Password
    ${date}                             Get Current Date        result_format=%Y%m%d%H%M%S%f
    Set Suite Variable                  ${CUSTOMER_EMAIL}       customer+${date}@mail.com
    Input Text                          ${EMAIL_ADDRESSS}       ${CUSTOMER_EMAIL}
    Log To Console                      INFO: Customer email:   ${CUSTOMER_EMAIL}
    Input Password                      ${PASSWORD_FIELD}       ${PASSWORD}

Submit Registration Form
    Wait Until Element Is Enabled       ${SUBMIT}
    Click Element                       ${SUBMIT}

Verify Dashboard Page Opened
    Wait Until Page Contains Element    ${DASHBOARD_AVATAR}
    Log To Console                      INFO: Dashboard page is opened
