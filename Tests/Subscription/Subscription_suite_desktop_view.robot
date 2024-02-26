*** Settings ***
Documentation  Smoke suite for Subscription feature on ${COUNTRY} domain: ${START_URL}
Metadata    ver.2.0
Library     BuiltIn
Library     pabot.PabotLib
Variables   ../../Variables/domains_var.py
Variables   ../../Variables/api_data.py
Resource    ../../Resources/Common.robot
Resource    ../../Resources/Customer_Sign_up.robot

Test Setup      ${DISPLAY}
Test Teardown   End Web Test


*** Variables ***
${BROWSER}           CHROME
${RUN_MODE}          local
${VIEW_MODE}         desktop_view
${START_URL}
${PASSWORD}          123qwe123QWE
${DISPLAY}           Begin Web Test On Local Display
${TEST_SCOPE}
${SELENIUM_SPEED_DEFAULT}  0 seconds
${IMPLICIT_WAIT_DEFAULT}  1 seconds
${TESTLEVELSPLIT}    ${True}


*** Test Cases ***
CUSTOMER SIGN UP: through "Sign up" button on Homepage
    [Documentation]  As a Guest user, I should be able to sign up as a Customer through "Sign up" button on Homepage
    ...              Cases covered by this suite:
    ...              - SIGN UP as a Customer.
    [Tags]  smoke-qa  smoke-prod  smoke-qa-short  smoke-prod-short  sign-up  customer-sign-up
    Given I Am a Guest User On Sign Up Page
    When I Submit The Registration Form
    Then I Get Dashboard Page Opened
    And I Verify User's Data
