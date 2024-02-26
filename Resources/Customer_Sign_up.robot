*** Settings ***
Resource  ../Resources/PO/Public/homepage.robot
Resource  ../Resources/PO/Public/signupChoose.robot
Resource  ../Resources/PO/Customer/customerSignup.robot
Resource  ../Resources/Common.robot


*** Keywords ***
I Am a Guest User On Sign Up Page
    Get Homepage
    Open Sign-Up Page
    Select Customer Sign Up

I Submit The Registration Form
    Input User Names
    Input Email Address And Password
    Submit Registration Form

I Get Dashboard Page Opened
    Verify Dashboard Page Opened

I Verify User's Data
    I Fetch Data With API
    Verify Returned Data

