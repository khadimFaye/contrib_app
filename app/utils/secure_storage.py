
from dotenv import load_dotenv, set_key
from jose import jwt, JWTError, exceptions
import os
from json import JSONDecodeError
import json
import time
from flet.security import encrypt, decrypt 
from secrets import token_hex




dotenv_path = '.env'
load_dotenv(dotenv_path, override=True)

secret_key = os.getenv('bit32_key')
#ALGORITHM = os.getenv('ALGORITHM')


def save_token(service_name:str, username : str, token : str):
    
    set_key(dotenv_path=dotenv_path, key_to_set='exp', value_to_set=json.dumps({'service_name' : service_name, 'user_name':username}))
    set_key(dotenv_path=dotenv_path, key_to_set='token', value_to_set=token)
    load_dotenv(dotenv_path)
    
   
def get_token(service_name:str, username:str):
    #carica file della variabile d'ambiene
    try:

       
        #serializza il json file 
        data = json.loads(os.getenv('exp','{}'))
        if data:
           if data['service_name'] == service_name and data['user_name'] == username:
             
               return os.getenv('token')
        return None
    except (KeyError, Exception) as e:
        print(str(e))
def delet_current_token(service_name:str, username :str):
    try:

        data = json.loads(os.getenv('exp'))
        if data.get('user_name') == username and service_name == data.get('service_name'):
            print('eliminato')
            return set_key(dotenv_path=dotenv_path, key_to_set='token', value_to_set='')
        return False
    except (JSONDecodeError, KeyError) as e:
        print(str(e))

# save_token("myservice", "user", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDSzIzMTAiLCJleHAiOjE3MjM0MTA2OTZ9.44tc_degRjmitRaMGsjUvryhKV_03Y6KTIl4lJkt5Uc")
