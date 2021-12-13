# Responsive Fight Testing Scripts
The testing scripts consists of two parts: API tests and Web portal tests.

## Requirements
- Python 3.6
- Selenium

## Limits
- API tests - no known expired token yet. To cover this, added test case "test_verify_token_static" will test a hardcoded token, and expectation changes automatically according to token expiry date. After 15th Dec 2021, this test case will verify expired token. (Valid token is verified in "test_verify_token_dynamic")
- API tests - cannot test Delete user as it is protected by "delete-key", which is not provided
- Web portal test - portal installed/started on local environment, but H_KEY is not supplied. The key is named as "x-hasura-admin-secret" in "gqlQuestionApi.js", and is needed to connect to production API's (databases)

## API Tests
The tests will be extended later to get new token for running the test itself, currently it uses a fixed authentication token which expires on 15th Dec 2021.
Feature to read new token from gmail is already available, and used in test cases. Reason not doing this right now, because if implemented, Python built-in class unittest.TestCase will generate a new token for every test cases, which may cause extra load on back-end server.

- APP Authenticate - gentoken: script will test scenarios which token should/shouldn't be generated, if the expected result is token should be generated, then script will read token from gmail to ensure the email can be sent to desired email account.

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
