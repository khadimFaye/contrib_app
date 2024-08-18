
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


def save_token(page, service_name:str, username : str, token : str, title = None):
    
    data = {
        'service_name' : service_name,
        'user_name' : username,
        'sub' : username,
        'token' : token,
        'admin':title
        }
    
    
    
    # with open('dotenv.json', 'w', encoding='utf-8') as file:
    try:
        page.client_storage.set('admin', title)
        page.client_storage.set('sub', username)
        page.client_storage.set('exp', encrypt(json.dumps(data, indent=5), secret_key))
            # encode_data = page.client_storage.get('sub')
            # data = decrypt(encode_data, secret_key) if encode_data is not None else None
            
            # if data!={}:
            #     encode_data = encrypt(json.dumps(data), secret_key)
            #     file.write(json.dumps({'sub':encode_data}, indent=5))
                
    except (FileNotFoundError, JSONDecodeError, Exception) as e :
        print(f"Error saving token: {e}")

   
def get_token(page, service_name:str, username:str = None):
    #carica file della variabile d'ambiene
    try:

       
        print('\n', ('utente',username))
        #serializza il json file 
        encode_data = page.client_storage.get('exp')
        data = json.loads(decrypt(encode_data, secret_key)) if encode_data is not None else None
        # print(page.client_storage.get('exp'))
        # with open('dotenv.json', 'r', encoding='utf-8') as file:
        #     wrapped_buffer = json.loads(file.read()).get('sub')
        #     encoded_data = decrypt(wrapped_buffer, secret_key)
        #     data = json.loads(encoded_data)
      
           
       
        if data.get('service_name') == service_name and data.get('sub')==username:
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

