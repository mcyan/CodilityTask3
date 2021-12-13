'''
Python 3.6    
Created on 12 Dec 2021

@author: li.yan
'''

import unittest
import requests
import json
import time
import reademail
import datetime

# the token is generated around 5pm 12/12/2021, will be expired in 3 days
# the tests could be switched later to automatically generate and use new token for running testing script. Feature to read/return new token from gmail is already available in "reademail.py"
# Reason not doing this right now, because if implemented, Python built-in class unittest.TestCase will generate a new token for every test cases
# which may cause extra load on back-end server, also reading new token from gmail for every test cases can significantly slow down the tests.
AUTH = r'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJseTIwMjExMjEyIiwiZW1haWwiOiJsaS15YW5AaG90bWFpbC5jb20iLCJpYXQiOjE2MzkyODM2OTIsImV4cCI6MTYzOTU0Mjg5Mn0.2tuhJr97DPsm0dha7tEQlkl6XOUnMv0Nn-9-MGtmNgzk-px-n1EGjx7IwQK29-DWQpd5KMcKBNm2H_-TUIbUUg'

BASEURL = r'https://supervillain.herokuapp.com'
GENTOKEN_URL = r'https://supervillain.herokuapp.com/auth/gentoken'
VRYTOKEN_URL = r'https://supervillain.herokuapp.com/auth/verifytoken'
LOGIN_URL = r'https://supervillain.herokuapp.com/auth/user/login'
REGISTER_URL = r'https://supervillain.herokuapp.com/auth/user/register'
USER_URL = r'https://supervillain.herokuapp.com/v1/user'

#TO-DO: change to inherit from "unittest.TestCase" to enable testing
class AppAuthGenerate(unittest.TestCase):    
#class AppAuthGenerate():
    '''
    Test Application Authentication API - Generate Token
    '''        
    def setUp(self):
    #TO-DO: if time allowed, should change to get new token via email (function is already available)
                        
        self.body = {}
        self.key = ''
        
        #self.URLGEN = BASEURL+r'/auth/gentoken'
        self.HEADERS = {
            r'accept': r'application/json',            
            r'Content-Type': r'application/json'
                        }
    
    def test_gen_verify_token_success(self):
        '''
        Test Application Authentication API - Generate Token
        Expected to successfully generate a new token using random 'key' and email 'crazyFrog@yopmail.com'        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_success')
        print ('Expected to successfully generate a new token using random "key" and email "crazyFrog@yopmail.com"')
        
        __email = r'responsivefight.win@gmail.com'
                                            
        # generate random key
        self.body['key']=int(time.time())        
        self.body['email']=__email                
        
        expected_code = r'200'        
        
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)                                
        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to generate new token! Response=" + str(r)
        
        # read token in gmail
        check_email = reademail.ReadeMail()
        
        tmp_token = check_email.readtoken() 
        
        assert len(tmp_token)>0, "Error - Token wasn't sent to expected email! Response=" + str(r.content)
        
        # Below script will call Verify Token using new token in email
        __body = {}
        __headers = {
            r'accept': r'application/json',
            r'Authorization': tmp_token                        
                        }
                                
        r = requests.get(VRYTOKEN_URL, data=json.dumps(__body), headers=__headers)                
        
        expected_code = r'200'                              
        assert str(r).lower().find(expected_code)>=0, r'Error - Failed to verify token! Response=' + str(r)                 
        
    
    def test_gen_token_success_key_50(self):
        '''
        Test Application Authentication API - Generate Token
        Expected to successfully generate a new token when key's length is 50 (maximum allowed)         
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_success_key_50')
        print ("Expected to successfully generate a new token when key's length is 50 (maximum allowed)")
        
        # generate random key
        __email = r'responsivefight.win@gmail.com'
                                    
        self.body['key']=str(int(time.time())).zfill(50)        
        self.body['email']=__email                
        
        expected_code = r'200'        
        
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)            
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to generate new token! Response=" + str(r)
        
        # read token in gmail
        check_email = reademail.ReadeMail()
        
        assert len(check_email.readtoken())>0, "Error - Token wasn't sent to expected email! Response=" + str(r.content)  
        
    def test_gen_token_fail_duplicate_key(self):
        '''
        Test Application Authentication API - Generate Token
        Expected not to generate a new token due to duplicate key "crazyFrog"        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_fail_duplicate_key')
        print ('Expected to fail to generate a new token due to duplicate key "crazyFrog"')
        
        # generate random key
        __email = r'crazyFrog@yopmail.com'
                            
        self.body['key'] = r'crazyFrog'        
        self.body['email'] = __email                
        
        expected_code = r'400'
        expected_res = r'error: duplicate key value'
                
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate duplicate key values! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)

    def test_gen_token_fail_duplicate_key_uppercase(self):
        '''
        Test Application Authentication API - Generate Token
        Expected not to generate a new token due to duplicate key "crazyFrog"        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_fail_duplicate_key_uppercase')
        print ('Expected to fail to generate a new token due to duplicate key "crazyFrog"')
        
        # generate random key
        __email = r'crazyFrog@yopmail.com'
                            
        self.body['key'] = r'CRAZYFROG'        
        self.body['email'] = __email                
        
        expected_code = r'400'
        expected_res = r'error: duplicate key value'
                
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate duplicate key values! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)

    def test_gen_token_fail_Long_key(self):
        '''
        Test Application Authentication API - Generate Token
        Expected to fail to generate a new token due to key length exceeds 50        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_fail_Long_key')
        print ('Expected not to generate a new token due to key length exceeds 50')        
        
        
        # generate random key
        __email = r'crazyFrog@yopmail.com'
                            
        self.body['key'] = r'012345678901234567890123456789012345678901234567891'        
        self.body['email'] = __email                
        
        expected_code = r'400'
        expected_res = r'error: value too long'
                
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate length of key! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)

    
    def test_gen_token_fail_invalid_email(self):
        '''
        Test Application Authentication API - Generate Token
        Expected to failed to generate a new token due to invalid email "crazyFrogyopmail.com"        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_fail_invalid_email')
        print ('Expected not to generate a new token due to invalid email "crazyFrogyopmail.com"')
        
        # generate random key
        __email = r'crazyFrogyopmail.com'
                            
        self.body['key']=int(time.time())        
        self.body['email'] = __email                
        
        expected_code = r'400'
        expected_res = r'error: '
                
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate email address (wrong format)! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)  
        
    
    # Commented out this test case, as it will lead to server crash down, can be re-enabled after the service issue is fixed
    # def test_gen_token_fail_missing_key(self):
    #     '''
    #     Test Application Authentication API - Generate Token
    #     Expected to failed to generate a new token due to key is not supplied        
    #     '''
    #     print ('/---------------------------------/')
    #     print ('Test Case: Application Authentication - test_gen_token_fail_missing_key')
    #     print ('Expected to failed to generate a new token due to key is not supplied')
    #
    #     # generate random key
    #     __email = r'crazyFrogyopmail.com'
    #
    #     self.body['key']=r''        
    #     self.body['email'] = __email                
    #
    #     expected_code = r'400'
    #     expected_res = r'error: '
    #
    #     r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
    #
    #     assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate key value (empty)! Response=" + str(r)
    #     assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)
        
    def test_gen_token_fail_missing_email(self):
        '''
        Test Application Authentication API - Generate Token
        Expected not to generate a new token due to email is not supplied        
        '''        
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_gen_token_fail_missing_email')
        print ('Expected to failed to generate a new token due to email is not supplied')
                        
        # generate random key
        __email = r''
                            
        self.body['key']=int(time.time())        
        self.body['email'] = __email                
        
        expected_code = r'400'
        expected_res = r'error: '
                
        r = requests.post(GENTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to validate email address (empty)! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)               

    def tearDown(self):
        pass


#TO-DO: change to inherit from "unittest.TestCase" to enable testing
class AppAuthVerify(unittest.TestCase):
#class AppAuthVerify():
    '''
    Test Application Authentication API - Verify Token    
    '''        
    def setUp(self):                        
        self.body = {}         
        self.HEADERS = {
            r'accept': r'application/json',                       
                        }                  
    
    def test_verify_token_dynamic(self):
        '''
        Expected to successfully generate a new token and then call API to verify it        
        '''
        # this is covered in test case: AppAuthGenerate.test_gen_verify_token_success
        pass
    
    def test_verify_token_static(self):
        '''
        Expected to successfully verify a token, the token is generated around 5pm 12/12/2021, therefore expected result varies depending on time        
        '''
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_verify_token_static')
        print ('Expected to successfully verify a token, the token is generated around 5pm 12/12/2021, therefore expected result varies depending on time')
        
        self.HEADERS['Authorization'] = AUTH                                                   
                
        r = requests.get(VRYTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)                
        
        expected_code = r'200'
        #expected_res = r'error: '
        
        now = datetime.datetime.now()
        
        if ((now.year==2021) | (now.month)==12):
            if now.day > 15:
                expected_code = r'400'
                expected_res = r'error: '
            else:
                expected_code = r'200'
                #expected_res = r'error: '     
                 
        assert str(r).lower().find(expected_code)>=0, r'Error - Failed to verify token! Response=' + str(r)
        #assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)               

    def test_verify_token_invalid_token(self):
        '''
        Expected to return 400 because token is invalid        
        '''        
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_verify_token_invalid_token')
        print ('Expected to return 400 because token is invalid')                                    
        
        expected_code = r'400'
        expected_res = r'error: '
        
        self.HEADERS['Authorization'] = r'yyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJseTIwMjExMjEyIiwiZW1haWwiOiJsaS15YW5AaG90bWFpbC5jb20iLCJpYXQiOjE2MzkyODM2OTIsImV4cCI6MTYzOTU0Mjg5Mn0.2tuhJr97DPsm0dha7tEQlkl6XOUnMv0Nn-9-MGtmNgzk-px-n1EGjx7IwQK29-DWQpd5KMcKBNm2H_-TUIbUUg'
                
        r = requests.get(VRYTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, r'Error - Failed to validate token! Response=' + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)    

    def test_verify_token_empty_token(self):
        '''
        Expected to return 400 because token is empty        
        '''        
        print ('/---------------------------------/')
        print ('Test Case: Application Authentication - test_verify_token_empty_token')
        print ('Expected to return 400 because token is empty')                                    
        
        expected_code = r'400'
        expected_res = r'error: '
        
        self.HEADERS['Authorization'] = r''
                
        r = requests.get(VRYTOKEN_URL, data=json.dumps(self.body), headers=self.HEADERS)
                
        assert str(r).lower().find(expected_code)>=0, r'Error - Failed to validate token! Response=' + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - request body is not expected! Response=" + str(r.content)  
                         
    def tearDown(self):
        pass


#TO-DO: change to inherit from "unittest.TestCase" to enable testing
class UserAuth(unittest.TestCase):
#class UserAuth():    
    '''
    Test User Authentication API
    '''        
    def setUp(self):
        #TO-DO: if time allowed, should change to get new token via email (function is already available)        
        self.body = {}
        self.reg_headers = {
            r'accept': r'*/*',
            r'Authorization':AUTH,
            r'Content-Type': r'application/json'
                        }
        self.login_headers = {
            r'accept': r'application/json',
            r'Authorization':AUTH,            
            r'Content-Type': r'application/json'
                        }        


    def test_register_success(self):
        '''
        Expected to successfully register a new account        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_success')        
        # generate random name        
                                    
        self.body['username']= r'LY'+str(int(time.time()))
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'200'
        #expected_res = r''
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)
        
        #print(r)            
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to create a new account! Response=" + str(r)
        #assert str(r.content).lower().find(expected_res)>=0, "Error - Token wasn't sent to expected email! Response=" + str(r.content)         
    
    def test_register_success_long_name_50(self):
        '''
        Expected to successfully register with long name        
        '''                                              
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_success_long_name_50')
        
        self.body['username']= r'LY'+str(int(time.time())).zfill(48)
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'200'
        #expected_res = r''
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to create a new account with 50 letters in name! Response=" + str(r)
        
    
    def test_register_fail_invalidtoken(self):
        '''
        Expected to return 401, as token is invalid        
        '''                
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_invalidtoken')
        
        self.body['username']= r'ly20211212'
        self.body['password']=r'string'                             
        
        expected_code = r'401'
        #expected_res = r'Token Authentication failed'
        
        __headers = {
            r'accept': r'*/*',
            r'Authorization':'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9',
            r'Content-Type': r'application/json'
                        }
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=__headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with 51 letters in name! Response=" + str(r)        
    
    def test_register_fail_empty_name(self):
        '''
        Expected to return 400 as user name is not supplied        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_empty_name')
        
        self.body['username']= r''
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'400'
        #expected_res = r''
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with empty name! Response=" + str(r)
        
    def test_register_fail_xtraLong_Name_51(self):
        '''
        Expected to return 400 as user name exceeds the length of defined field in code        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_xtraLong_Name_51')
        
        self.body['username']= r'LY'+str(int(time.time())).zfill(49)
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'400'
        #expected_res = r''
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with 51 letters in name! Response=" + str(r)
    
    def test_register_fail_simple_password(self):
        '''
        Expected to return 400 add a new user with long name        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_simple_password')
        
        self.body['username']= r'LY'+str(int(time.time())).zfill(48)
        self.body['password']=r'12345678'                             
        
        expected_code = r'400'        
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with simple password! Response=" + str(r)
    
    def test_register_fail_empty_password(self):
        '''
        Expected to return 400 as password is not supplied        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_empty_password')
        
        self.body['username']= r'LY'+str(int(time.time())).zfill(48)
        self.body['password']=r''                             
        
        expected_code = r'400'        
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with Empty password! Response=" + str(r)
    
    def test_register_fail_existing_username(self):
        '''
        Expected to return 400 as username already exists        
        '''        
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_existing_username')
        
        self.body['username']= r'ly20211212'
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'400'
        #expected_res = r'already exists'        
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with existing name! Response=" + str(r)          

    def test_register_fail_existing_username_uppercase(self):
        '''
        Expected to return 400 as username already exists        
        '''        
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_register_fail_existing_username_uppercase')
        
        self.body['username']= r'LY20211212'
        self.body['password']=r'1234-cba'                             
        
        expected_code = r'400'               
        
        r = requests.post(REGISTER_URL, data=json.dumps(self.body), headers=self.reg_headers)            
        #print(r)        
        assert str(r).lower().find(expected_code)>=0, "Error - Should NOT allow to create a new account with existing name! Response=" + str(r)          


    def test_login_success_upper(self):
        '''
        Expected to return 200        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_login_success_upper')        
                
                                    
        self.body['username']= r'LY20211212'
        self.body['password']=r'string'                             
        
        expected_code = r'200'
        expected_res = r'token'
        
        r = requests.post(LOGIN_URL, data=json.dumps(self.body), headers=self.login_headers)
        
        print(r)            
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to login as LY20211212 (upper case)! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - unexpected return message! Response=" + str(r.content)         
    
    def test_login_success_lower(self):
        '''
        Expected to return 200        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_login_success_lower')        
                
                                    
        self.body['username']= r'ly20211212'
        self.body['password']=r'string'                             
        
        expected_code = r'200'
        expected_res = r'token'
        
        r = requests.post(LOGIN_URL, data=json.dumps(self.body), headers=self.login_headers)
        
        #print(r)            
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to login as ly20211212 (lower case)! Response=" + str(r)
        assert str(r.content).lower().find(expected_res)>=0, "Error - unexpected return message! Response=" + str(r.content)         
    
    def test_login_fail_invalidtoken(self):
        '''
        Expected to return 401, as token is invalid        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_login_fail_invalidtoken')
        
        self.body['username']= r'ly20211212'
        self.body['password']=r'string'                             
        
        expected_code = r'401'
        #expected_res = r'Token Authentication failed'
        
        __headers = {
            r'accept': r'application/json',
            r'Authorization':'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9',
            r'Content-Type': r'application/json'
                        }
        
        r = requests.post(LOGIN_URL, data=json.dumps(self.body), headers=__headers)
                
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to login as ly20211212 (lower case)! Response=" + str(r)            
        
    def test_login_fail_password_case_sensitive(self):
        '''
        Expected to return 400, as token is invalid        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_login_fail_password_case_sensitive')        
                
                                    
        self.body['username']= r'ly20211212'
        self.body['password']=r'String'                             
        
        expected_code = r'400'
        #expected_res = r'Username or Password is incorrect'
        
        r = requests.post(LOGIN_URL, data=json.dumps(self.body), headers=self.login_headers)
                
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow login as password is upper case! Response=" + str(r)
        #assert str(r.content).lower().find(expected_res)>=0, "Error - unexpected return message! Response=" + str(r.content)         

    
    def test_login_fail_sql_injection(self):
        '''
        Expected to return 400, as token is invalid        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Authentication - test_login_fail_sql_injection')        
                
                                    
        self.body['username']= r'ly20211212'
        self.body['password']="' or '1'='1"                             
        
        expected_code = r'400'
        #expected_res = r'Username or Password is incorrect'
        
        r = requests.post(LOGIN_URL, data=json.dumps(self.body), headers=self.login_headers)
                
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow login as password is incorrect! Response=" + str(r)
        #assert str(r.content).lower().find(expected_res)>=0, "Error - unexpected return message! Response=" + str(r.content)         
    
    def tearDown(self):
        pass



#TO-DO: change to inherit from "unittest.TestCase" to enable testing
class UserLeaderboard(unittest.TestCase):
#class UserAuth():    
    '''
    Test User Leaderboard API
    '''        
    def setUp(self):
        #TO-DO: if time allowed, should change to get new token via email (function is already available)        
        self.body = {}
        
        self.g_headers = {
            r'accept': r'application/json',
            r'Authorization':AUTH,            
                        }
        self.p_headers = {            
            r'accept': r'*/*',
            r'Authorization':AUTH,            
            r'Content-Type': r'application/json'
                        }


    def test_add_list_success(self):
        '''
        Expected to successfully add a new user, return in list        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_list_success')        
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY'+ str(__random_number)
        self.body['score']=__random_number                             
        
        expected_code = r'201'
        #expected_res = r'success'
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to create a new user! Response=" + str(r)
        
        # check if new user can be returned in list
        expected_code = r'200'
        __headers = {}
        r = requests.get(USER_URL, data=json.dumps(__headers), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to fetch the user list! Response=" + str(r)
                
        # verify if new user name show in list
        __expected_res = str(self.body['username']).lower()
        assert str(r.content).lower().find(__expected_res)>=0, "Error - New user is not returned! Response=" + str(r.content)      
        # verify if user's score is correct
        __expected_res = str(__random_number)
        assert str(r.content).find(__expected_res)>=0, "Error - New user's score is not returned! Response=" + str(r.content)


    def test_add_fail_no_score(self):
        '''
        Expected not to allow adding a new user with no score        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_success_no_score')        
                
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY'+ str(__random_number)
        self.body['score']=''                             
        
        expected_code = r'400'
        #expected_res = r'Error'
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with no score! Response=" + str(r)
        

    def test_add_fail_empty_name(self):
        '''
        Expected not to allow adding a new user with empty username        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_empty_name')
                
                                                    
        self.body['username']= ''
        self.body['score']=123                             
        
        expected_code = r'400'        
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with empty username! Response=" + str(r)

    def test_add_fail_duplicate_name_case_insensitive(self):
        '''
        Expected not to allow adding a new user with same username but upper/lower cases        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_duplicate_name_case_insensitive')
        
        # add a new user first
        __random_number = int(time.time())                                                    
        self.body['username']= r'LY'+ str(__random_number)                
        self.body['score']=1                             
        
        expected_code = r'201'                
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to add a new user! Response=" + str(r)
        
        # add the same name with lower case
        self.body['username']= r'ly'+ str(__random_number)                                                      
        expected_code = r'400'                
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with same username but upper/lower cases! Response=" + str(r)

    def test_add_fail_duplicate_name(self):
        '''
        Expected not to allow adding a new user with a username already exists        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_duplicate_name')        
        
        self.body['username']= 'LY20211212'
        self.body['score']=123                             
        
        expected_code = r'400'
        #expected_res = r'error: duplicate key value violates unique constraint'        
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with same username! Response=" + str(r)        
        
    def test_add_fail_long_name_51(self):
        '''
        Expected not to allow adding a new user with 51 charactors in username        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_long_name_51')
        
        self.body['username']= r'LY'+str(int(time.time())).zfill(49)
        self.body['score']=123                             
        
        expected_code = r'400'                
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with more than 51 charactors in name! Response=" + str(r)  
    
    def test_add_fail_score_letter(self):
        '''
        Expected not to allow adding a new user with letter in score        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_score_letter')
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY'+ str(__random_number)
        self.body['score']='A'                             
        
        expected_code = r'400'        
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with score 'A'! Response=" + str(r)
                

    def test_add_fail_score_minus(self):
        '''
        Expected not to allow adding a new user with minus score        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_score_minus')
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY'+ str(__random_number)
        self.body['score']=-10                             
        
        expected_code = r'400'        
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with minus score! Response=" + str(r)
                
            
    def test_add_fail_large_score_2147483648(self):
        '''
        Expected not to allow adding a user with score to more than integer supported        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_large_score_2147483648')
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY'+ str(__random_number)
        self.body['score']=2147483648                             
        
        expected_code = r'400'        
        
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with score 2147483648! Response=" + str(r)    
    
    
    def test_update_list_success(self):
        '''
        Expected to successfully update a user, and return in list        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_list_success')        
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY20211212'
        self.body['score']=__random_number                             
        
        expected_code = r'204'
        #expected_res = r'success'
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to update user's score! Response=" + str(r)
        
        # check if new user can be returned in list
        expected_code = r'200'
        __headers = {}
        r = requests.get(USER_URL, data=json.dumps(__headers), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to fetch the user list! Response=" + str(r)
                              
        # verify if user's score is correct
        __expected_res = str(__random_number)
        assert str(r.content).find(__expected_res)>=0, "Error - user's score is not updated! Response=" + str(r.content)


    def test_update_new_user_success(self):
        '''
        Expected to successfully add a new user as username cannot be found        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_new_user_success')        
        
        # generate random name
        __random_number = int(time.time())
                                                    
        self.body['username']= r'LY20211212'+str(__random_number)
        self.body['score']=__random_number                             
        
        expected_code = r'201'
        #expected_res = r'success'
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to add user when update cannot find the matched username! Response=" + str(r)
        
        # check if new user can be returned in list
        expected_code = r'200'
        __headers = {}
        r = requests.get(USER_URL, data=json.dumps(__headers), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to fetch the user list! Response=" + str(r)
                
        # verify if new user name show in list
        __expected_res = str(self.body['username']).lower()
        assert str(r.content).lower().find(__expected_res)>=0, "Error - New user is not returned! Response=" + str(r.content)      
        # verify if user's score is correct
        __expected_res = str(__random_number)
        assert str(r.content).find(__expected_res)>=0, "Error - New user's score is not returned! Response=" + str(r.content)


    def test_update_fail_no_score(self):
        '''
        Expected not to allow updating a user with no score        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_fail_no_score')        
                        
        self.body['username']= r'LY20211212'
        self.body['score']=''                             
        
        expected_code = r'400'
        #expected_res = r'Error'
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow updating a user with no score! Response=" + str(r)
        

    def test_update_fail_empty_name(self):
        '''
        Expected not to allow update with empty username        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_fail_empty_name')
                
                                                    
        self.body['username']= ''
        self.body['score']=123                             
        
        expected_code = r'400'        
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow updating a user with empty username! Response=" + str(r)

    def test_update_sucess_name_case_insensitive(self):
        '''
        Expected to update existing user's score, even given username has different upper/lower cases        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_sucess_name_case_insensitive')
        
        # add a new user first
        __random_number_1 = int(time.time())                                                    
        self.body['username']= r'LY'+ str(__random_number_1)                
        self.body['score']=__random_number_1                             
        
        expected_code = r'201'                
        r = requests.post(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - Failed to add a new user! Response=" + str(r)
        
        # Update the same name with lower case
        self.body['username']= r'ly'+ str(__random_number_1)
        __random_number_2 = int(time.time())
        self.body['score']=__random_number_2
                                                              
        expected_code = r'204'                
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow adding a new user with same username but upper/lower cases! Response=" + str(r)                  
    
    def test_update_fail_score_letter(self):
        '''
        Expected not to allow updating score to a letter        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_fail_score_letter')
                                
        self.body['username']= r'LY20211212'
        self.body['score']='A'                             
        
        expected_code = r'400'        
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow change score to 'A'! Response=" + str(r)
                

    def test_update_fail_score_minus(self):
        '''
        Expected not to allow changing score to minus number        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_update_fail_score_minus')
                
        self.body['username']= r'LY20211212'
        self.body['score']=-10                             
        
        expected_code = r'400'        
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow changing score to minus number! Response=" + str(r)
                
            
    def test_update_fail_large_score_2147483648(self):
        '''
        Expected not to allow change score to more than integer supported        
        '''
        print ('/---------------------------------/')
        print ('Test Case: User Leaderboard - test_add_fail_large_score_2147483648')
        
        self.body['username']= r'LY20211212'
        self.body['score']=2147483648                             
        
        expected_code = r'400'        
        
        r = requests.put(USER_URL, data=json.dumps(self.body), headers=self.p_headers)                        
        assert str(r).lower().find(expected_code)>=0, "Error - should not allow changing score to 2147483648! Response=" + str(r)

                            
    def tearDown(self):
        pass


if __name__ == "__main__": 
    unittest.main()