*** Settings ***
Library     SeleniumLibrary
Resource    ../../Common.robot
Resource    signupChoose.robot


*** Variables ***
${SEARCH_CTA}                           //*[@data-cy="CI_searchAutocomplete_searchCta"]
${SIGN_UP_CTA}                          class=header_mainNavigation_chooseAccountRoute


*** Keywords ***
Get Homepage
    Go To                               ${START_URL}
    Wait Until Page Contains Element    ${SEARCH_CTA}

Open Sign-Up Page
    Click Element                       ${SIGN_UP_CTA}
    Wait Until Page Contains Element    ${SIGN_UP_USER}














Verify Homepage Loaded
    Wait Until Page Contains Element    ${search-input}

Verify SEO tags
    ${actual_page_title}                get title
    Should Be Equal                     ${actual_page_title}  ${page_title}
    Log To Console                      INFO: Title tag checked
    element attribute value should be   tag=meta  content  ${page_meta}
    Log To Console                      INFO: Meta tag checked
    Run Keyword If  "${ENV}" == "prod"    Wait Until Page Contains Element    //link[contains(@href, 'https://www.starofservice.com/')]
    ...  ELSE IF    "https://qa.starofservice" in "${START_URL}"  Wait Until Page Contains Element    //link[contains(@href, 'https://qa.starofservice.com/')]
    Run Keyword If  "${ENV}" == "prod"    Wait Until Page Contains Element    //link[contains(@href, 'https://www.starofservice.com.br/')]
    ...  ELSE IF    "https://qa.starofservice" in "${START_URL}"  Wait Until Page Contains Element    //link[contains(@href, 'https://qa.starofservice.com.br/')]
    Run Keyword If  "${ENV}" == "prod"    Wait Until Page Contains Element    //link[contains(@href, 'https://www.starofservice.es/')]
    ...  ELSE IF    "https://qa.starofservice" in "${START_URL}"  Wait Until Page Contains Element    //link[contains(@href, 'https://qa.starofservice.es/')]
    Log To Console                      INFO: SEO links checked
    Wait Until Page Contains Element    css=a[data-test="region-0_link"]
    Log To Console                      INFO: Region links checked

Accept cookies
    wait until element is visible       ${cookie_banner_accept}
    click button                        ${cookie_banner_accept}
    wait until page does not contain element  ${cookie_banner_accept}
    Log To Console                      INFO: Cookie banner submitted

Check Homepage and close covid banner
    wait until element is visible       ${covid_banner_close_button}
    Click Element                       ${covid_banner_close_button}
    ${covid_banner_off}                 Run Keyword And Return Status  wait until element is not visible  ${covid_banner_close_button}
    run keyword unless                  ${covid_banner_off}  Submit banner using JS
    wait until page does not contain element  ${covid_banner_close_button}
    Log To Console                      INFO: COVID banner submitted

Submit banner using JS
    execute javascript                  document.querySelector('[data-test="covid_banner.close"]').click()
    Log To Console                      INFO: Submitting banner using JS

Enter service to the search bar on Homepage
    input text                          ${search-input}  ${SERVICE}
    wait until element is visible       //div[@data-test="${pokemon_go_slug}"]  timeout=40
    Click Element                       //div[@data-test="${pokemon_go_slug}"]

Click on Pro signup button
    Click Element                       ${join_as_pro_button}

Click on Log in button
    click link                          ${login_button}

Scroll to footer
    execute javascript                  window.scrollBy(900, 900)

Click on Homepage "About" button
    Run Keyword If                      "${COUNTRY_CODE}" == "fr"   Accept cookies
    wait until element is visible       ${about_link}
    set focus to element                ${about_link}
    click link                          ${about_link}

Click on Homepage "Autopilot" button
    wait until element is visible       ${autopilot_link}
    set focus to element                ${autopilot_link}
    click link                          ${autopilot_link}

Click on "Pro How it works" button
    wait until element is visible       ${how_it_works_pro_link}
    set focus to element                ${how_it_works_pro_link}
    click link                          ${how_it_works_pro_link}

Click on "Testimonials" button on homepage footer
    wait until element is visible       ${success_stories_link}
    set focus to element                ${success_stories_link}
    click link                          ${success_stories_link}


Click Homepage annubis region link "Ile-de-France"
    accept cookies
    click link                          ${region-13_link}

Click Homepage "Extra services" tab
    click link                          ${select_service.categories.more}

Click "Coach sport" service
    Wait Until Page Contains Element    ${coach_sport_service_block}
    Click Element                       ${coach_sport_service_block}

# =============================================================================================|
# ====================================== MOBILE VIEW: =========================================|
# =============================================================================================|
Open homepage left-top menu
    click link                          ${mobile_header_home-link}

Verify homepage left-top menu opened
    Wait Until Element Is Enabled       ${mobile_join_as_pro_button}

Open Sign-Up Page [mobile view]
    click link                          ${mobile_sign_up_button}

Click on Pro signup button [mobile view]
    click link                          ${mobile_join_as_pro_button}

Click on Log in button [mobile view]
    click link                          ${mobile_login_button}

Click on Homepage "About" button [mobile view]
    Run Keyword If                      "${COUNTRY_CODE}" == "fr"   Accept cookies
    execute javascript                  document.evaluate('//footer/div/div[1]/div[1]/div/div[1]',document.body,null,9,null).singleNodeValue.click();
    wait until element is visible       ${about_link}
    set focus to element                ${about_link}
    click link                          ${about_link}

Click on "Pro How it works" button [mobile view]
    execute javascript                  document.evaluate('//footer/div/div[1]/div[3]/div/div[1]',document.body,null,9,null).singleNodeValue.click();
    wait until element is visible       ${how_it_works_pro_link}
    set focus to element                ${how_it_works_pro_link}
    click link                          ${how_it_works_pro_link}

Click on "Testimonials" button on homepage footer [mobile view]
    execute javascript                  document.evaluate('//footer/div/div[1]/div[3]/div/div[1]',document.body,null,9,null).singleNodeValue.click();
    wait until element is visible       ${success_stories_link}
    set focus to element                ${success_stories_link}
    click link                          ${success_stories_link}

Click on Homepage "Autopilot" button [mobile view]
    execute javascript                  document.evaluate('//footer/div/div[1]/div[3]/div/div[1]',document.body,null,9,null).singleNodeValue.click();
    wait until element is visible       ${autopilot_link}
    set focus to element                ${autopilot_link}
    click link                          ${autopilot_link}

Click Homepage "Extra services" tab [mobile view]
    Go To                               ${START_URL}extra-services  #TODO: to improve