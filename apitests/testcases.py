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
AUTH = r'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJseTIwMjExMjEyIiwiZW1haWwiOiJsaS15YW5AaG90bWFpbC5jb20iLCJpYXQiOjE2MzkyODM2OTIsImV4cCI6MTYzOTU0Mjg5Mn0.2tuhJr97DPsm0dha7tEQlkl6XOUnMv0Nn-9-MGtmNgzk-px-n1EGjx7IwQK29-DWQpd5KMcKBNm2H_-TUIbUUg'

BASEURL = r'https://supervillain.herokuapp.com'
GENTOKEN_URL = r'https://supervillain.herokuapp.com/auth/gentoken'
VRYTOKEN_URL = r'https://supervillain.herokuapp.com/auth/verifytoken'

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
#class UserAuth(unittest.TestCase):
class UserAuth():    
    '''
    Test User Authentication API
    '''        
    def setUp(self):
        #TO-DO: if time allowed, should change to get new token via email (function is already available)
        self.URL = BASEURL+r'/v1/user'
        self.body = {}
        self.HEADERS = {
            r'accept': r'*/*',
            r'Authorization':AUTH,
            r'Content-Type': r'application/json'
                        }        

    def test_add_user_success(self):
        '''
        Expected to successfully add a new user        
        '''
        # generate random name        
        pass        
            

    def tearDown(self):
        pass


if __name__ == "__main__": 
    unittest.main()