# Responsive Fight Testing Scripts
The testing scripts consists of two parts: API tests and Web portal tests.

## Requirements
- Python 3.6
- Selenium

## Limits & Risks
- Web portal test - portal installed/started on local environment, but H_KEY is not supplied. The key is named as "x-hasura-admin-secret" in "gqlQuestionApi.js", and is needed to connect to production API's (databases). Therefore, can only execute tests on login screen, and some of the tests are impossible to verify the outcome at this stage.
- API tests - the server might crash after negative test, and the failure is very random. When the issue occurs, all subsequent tests will get 503 from API call, and tests fail. Might need to run tests separately, and each time run a small sub-set of tests, to bypass the system error.
- API tests - cannot test Delete user as it is protected by "delete-key", which is not provided
- API tests - no known expired token yet. To cover this, added test case "test_verify_token_static" will test a hardcoded token, and expectation changes automatically according to token expiry date. After 15th Dec 2021, this test case will verify expired token. (Valid token is verified in "test_verify_token_dynamic")


## API Tests
Currently it uses a fixed authentication token which expires on 15th Dec 2021, the tests could be switched later to automatically generate and use new token for running testing script. Feature to read/return new token from gmail is already available in "reademail.py", and is used in some test cases. 

Reason not doing this right now, because if implemented, Python built-in class unittest.TestCase will generate a new token for every test cases, which may cause extra load on back-end server, also reading new token from gmail for every test cases can significantly slow down the tests.

Please refer to comments in testcases.py file in each folder for more details

## Web Tests
Webportal tests requires Selenium Webdriver for corresponding browser, tests are consist of static and functional tests.
As mentioned in "Limits" above, the portal cannot connect to production API, therefore, no futher tests after login.

## Start Test
Download this repo
- open testcases.py in corresponding folder in any IDE compatible with Python, execute from IDE
or
- run testcases.py in command-line

## Report
Due to the time limit, the outcome of tests will be printed on screen via Python class unittest, including the total number of test cases executed and how many failed.

e.g.

\-----------------------------------------------------

Ran 7 tests in 26.160s

FAILED (failures=5)
