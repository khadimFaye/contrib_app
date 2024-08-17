
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
    
    data = {
        'service_name' : service_name,
        'user_name' : username,
        'token' : token
        }
    
    
    with open('dotenv.json', 'w', encoding='utf-8') as file:
        try:
            
            if data!={}:
                encode_data = encrypt(json.dumps(data), secret_key)
                file.write(json.dumps({'sub':encode_data}, indent=5))
                
        except (FileNotFoundError, JSONDecodeError, Exception) as e :
            print(f"Error saving token: {e}")
    
   
def get_token(service_name:str, username:str):
    #carica file della variabile d'ambiene
    try:

       
        #serializza il json file 
        with open('dotenv.json', 'r', encoding='utf-8') as file:
            wrapped_buffer = json.loads(file.read()).get('sub')
            encoded_data = decrypt(wrapped_buffer, secret_key)
            data = json.loads(encoded_data)
      
           
       
        if data.get('service_name') == service_name and data.get('user_name') == username:
            return data.get('token')
        return None
    except (KeyError, Exception) as e:
        print(str(e))
        
# def delet_current_token(service_name:str, username :str):
#     try:

#         data = json.loads(os.getenv('exp'))
#         if data.get('user_name') == username and service_name == data.get('service_name'):
#             print('eliminato')
#             return set_key(dotenv_path=dotenv_path, key_to_set='token', value_to_set='')
#         return False
#     except (JSONDecodeError, KeyError) as e:
#         print(str(e))

