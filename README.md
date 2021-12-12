# Responsive Fight Testing Scripts
The testing scripts consists of two parts: API tests and Web portal tests.

## Requirements
- Python 3.6
- Selenium

## API Tests
- APP Authenticate - gentoken: script will test scenarios which token should/shouldn't be generated, and read token from gmail to ensure the email can be sent to desired email account. The feature will be extended later to get new token for running the test itself (currently it used a fixed authentication, will expire in 3 days)

- APP Authenticate - verifytoken

- User Authenticate


## Start Test
Download this repo
- open testcases.py in corresponding folder in any IDE compatible with Python, execute from IDE
or
- run testcases.py in command-line

## Report
Due to the time limit, the outcome of tests will be printed on screen, and Python class unittest will display the total number of test cases executed and how many failed.

e.g.

\-----------------------------------------------------

Ran 7 tests in 26.160s

FAILED (failures=5)
