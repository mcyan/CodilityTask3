'''
Python 3.6    
Created on 12 Dec 2021

@author: li.yan
'''
import time
import imaplib
import email




class ReadeMail(object):
    '''
    read email
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass                
    
    def readtoken(self):
        '''
        read token from most recent email
        '''
        self.EMAIL = "responsivefight.win@gmail.com" 
        self.PWD = "1234-gmail" 
        self.SMTP_SERVER = "imap.gmail.com" 
        self.PORT = 993
        
        token=''
                        
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.EMAIL, self.PWD)            
            
            #wait for 5 seconds
            time.sleep(5)
            
            print ('Waiting for email to be received......')
            i = 0
            while (i<=10):
                mail.select(r'inbox')
                data = mail.search(None, 'UnSeen')
                #data = mail.search(None, 'ALL')
                mail_ids = data[1]
                id_list = mail_ids[0].split()   
                if (len(id_list))>0:
                    break
                else:
                    i += 1
                    time.sleep(3)
            else:
                raise RuntimeError('email is not received!') 
                        
            data = mail.fetch(str(int(id_list[-1])), r'(RFC822)' )
            for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1],'utf-8'))                                                                                         
                        for part in msg.walk():
                            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                                message = part.get_payload(decode=True)                                
                                content = message.decode()
                                #print (str(content))                                
                                if str(content).find(r'Congratulations your application is register and the tokeKey is ')>=0:
                                    token = content[64:]
                                    #print("Token: ", token) 
                                    break
            
        except Exception as e:
            print(str(e))                    
        
        # close the mailbox
        mail.close()
        # logout from the account
        mail.logout()
        
        return token
        

# new = ReadeMail()
# print(new.readtoken())