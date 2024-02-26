*** Settings ***
Library     BuiltIn
Library     SeleniumLibrary
Resource    ../Customer/customerSignup.robot


*** Variables ***
${SIGN_UP_USER}                         //*[@data-cy="CI_chooseAccount_createCustomerAccountButton"]


*** Keywords ***
Select Customer Sign Up
    Click Element                       ${SIGN_UP_USER}
    Wait Until Page Contains Element    ${FIRST_NAME}

