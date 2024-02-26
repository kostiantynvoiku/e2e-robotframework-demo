*** Settings ***
Library  BuiltIn
Library  Collections
Library  OperatingSystem
Library  DateTime
Library  SeleniumLibrary
Library  RequestsLibrary
Library  ../Libraries/uuidLibrary.py
Library  ../Libraries/MimesisLibrary.py
Library  pabot.PabotLib
Library  ../Libraries/jsonlib.py
Library  ../Libraries/desired_caps.py
Resource  API_Requests.robot


*** Variables ***
${WIDTH}                1920
${HEIGHT}               1080


*** Keywords ***
Begin Web Test On Local Display
    Open Browser                        about:blank
    ...                                 ${BROWSER}
    # ...                               desired_capabilities=${chrome_desired_caps}
    Maximize Browser Window
    # set window size                   ${WIDTH}  ${HEIGHT}
    Set Selenium Timeout                20 seconds
    Set Selenium Implicit Wait          1s

Begin Web Test In Selenoid
    [Arguments]                         ${enableVideo}=${False}  ${dev_shm}=${False}  ${view_mode_arg}=desktop_view
    ${url_hub}                          Set Variable If  '${RUN_MODE}' == 'local'
    ...                                                   http://localhost:4444/wd/hub
    ...                                                   http://172.31.7.59:4444/wd/hub
    Set Suite Variable                  ${URL_HUB}
    Start Selenoid Session Chrome       ${enableVideo}  ${view_mode_arg}
    Maximize Browser Window
    Set Selenium Implicit Wait          1 seconds
    Set Selenium Timeout                20 seconds
    Log To Console                      INFO: ${BROWSER} session is run by Selenoid on ${VIEW_MODE} ${RUN_MODE}

Begin Web Test On Mobile Emulator
    [Arguments]                         ${view_mode_arg}
    ${mobile emulation}                 create dictionary    deviceName=iPhone X
    ${chrome options}                   Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()
    ...                                 sys, selenium.webdriver
    Call Method                         ${chrome options}    add_experimental_option    mobileEmulation    ${mobile emulation}
    Create Webdriver                    Chrome    chrome_options=${chrome options}
    Set Selenium Timeout                20 seconds
    Set Selenium Implicit Wait          1 seconds
    Set Suite Variable                  ${view_mode}       mobile_view

End Web Test
    Collect Logs if test failed
    Close All Browsers

Collect Logs if test failed
    ${is_active_session}  Assert WebDriver Session Is Active
    Run Keyword If  ${is_active_session}  Collect Logs

Assert WebDriver Session Is Active
    ${status}  ${message}  Run Keyword And Ignore Error  Get Window Identifiers
    Return From Keyword If
    ...  "${status}" == "FAIL"
    ...   ${False}
    RETURN  ${True}

Collect Logs
    Run Keyword If Test Failed  log location
    Run Keyword If Test Failed  log source
    Run Keyword If Test Failed  Common.Get HAR Log

Delete cookies
    Delete All Cookies
    Log To Console                      INFO: Cookies cleared

Start Selenoid Session Chrome
    [Arguments]                         ${enableVideo}=${False}  ${view_mode_arg}=desktop_view
    ${chrome_desired_caps}              set capabilities         ${view_mode_arg}
    set to dictionary                   ${chrome_desired_caps['selenoid:options']}  enableVideo  ${enableVideo}
    open browser                        about:blank
    ...                                 ${BROWSER}
    ...                                 remote_url=${URL_HUB}
    ...                                 desired_capabilities=${chrome_desired_caps}

Get HAR Log
    ${har_log}          execute async javascript    JAVASCRIPT  ${js_get_har}  ARGUMENTS  GET_HAR_SCRIPT
    ${current_date}     Get Current Date           result_format=%Y%m%d%H%M%S
    Create File         ${EXEC_DIR}/results/har_logs/${TEST NAME}_${current_date}.har
    Update Json         ${EXEC_DIR}/results/har_logs/${TEST NAME}_${current_date}.har  ${har_log}

Generate Fixtures
    ${identifier}  Get Current Date  result_format=%Y%m%d+
    Set Suite Variable        ${IDENTIFIER}
    Set Parallel Value For Key  IDENTIFIER  ${IDENTIFIER}
    ${order_by}             Set Variable If  '${COUNTRY_CODE}' == 'eg'  ASC  DESC
    ${city_id}              Set Variable        326001
    ${city_uuid}            Get Uuid From Id    ${city_id}  ${COUNTRY_CODE}
    Set Suite Variable      ${CITY_UUID}        ${city_uuid}
    ${zip_code}             Set Variable        1070
    ${city}                 Set Variable        Anderlecht
    ${landing_url}          Set Variable        annubis/bruxelles-capitale/region-bruxelles-capitale/anderlecht/pokemon-go
    ${landing_page}         Set Variable        ${START_URL}${landing_url}
    ${location}             Set Variable If
    ...                     "${COUNTRY_CODE}" == "vn"       ${zip_code}
    ...                     ${{ len('${zip_code}') > 0 }}   ${zip_code} ${city}
    ...                                                     ${city}
    Set Parallel Value For Key  CITY_UUID       ${city_uuid}
    Set Parallel Value For Key  ZIP_CODE        ${zip_code}
    Set Parallel Value For Key  CITY            ${city}
    Set Parallel Value For Key  LOCATION        ${location}
    Set Parallel Value For Key  LANDING_PAGE    ${landing_page}
    Log To Console              \n${{'=' *78}} \nSUITE SETUP: \n${SPACE*4}FETCHING LOCATION DATA: \n${SPACE*8}* City UUID: ${city_uuid} \n${SPACE*8}* Location: '${location}' \n${SPACE*8}* Landing page: ${landing_page} \n${{'=' *78}}

Fetch Fixtures
    Acquire Lock            suite_setup
    Run Setup Only Once     Generate Fixtures
    ${location_vars}        Create List  CITY_UUID  ZIP_CODE  CITY  LOCATION  LANDING_PAGE  IDENTIFIER
    Append To List  ${location_vars}  PRO_EMAIL  PRO_UUID  PRO_ID  PRO_SHORT_NAME  LIVE_CASE  SUBSCRIPTION_OFFER_IDENTIFIER  SUBSCRIPTION_OFFER_ID
    FOR  ${i}  IN  @{location_vars}
        ${a}  Get Parallel Value For Key  ${i}
        Set Suite Variable  ${${i}}  ${a}
    END
    Release Lock            suite_setup