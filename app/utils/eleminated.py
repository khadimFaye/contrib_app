# from cryptography.fernet import Fernet
# import os
# from typing import Annotated
# from dataclasses import dataclass
# import subprocess
# import base64

# '''
# this is a module that contain set of class and methodes to cache token locally after encrypted it in a save place
# and it create a virtual enviroment and activate 
# AUTHOR : FAYE KHADIM 
# DATE : 23/05/2024
# TIME : 22:28



# '''


# # def create_env():
# #     try:
# #         if os.path.exists('env'):
# #             print('Ã© gia presente un env ho un file chiamato env')
# #         else:
# #             subprocess.run(args='python.exe -m venv env', shell=True)
# #             print(r'copy this commnd in paste to CL to activate the env : .\env\Scripts\activate.bat')
# #     except Exception as e:
# #         pass

# # def activate_venv():
# #     if os.path.exists('env'):
# #         executible = os.path.join(os.getcwd(), 'env', 'Scripts','activate')
# #         # print(executible)
# #         subprocess.run(args='cd ../.',shell=True)
# # # create_env()
# # def make_essensials():
# #     path = os.path.join(os.getcwd(), 'env','Lib','secret')
# #     try:
        
# #         if not os.path.exists(path):
# #             os.chdir(os.path.join(os.getcwd(), 'env','Lib'))
# #             os.makedirs(path)
# #     except FileNotFoundError as e:
     
# #         return make_essensials()
# # make_essensials()

# ___key_file_name = 'key'
# __key_format = '.key'


# class IO(object):
#     def __init__(self, **args):
#         pass

#     @staticmethod    
#     def save_data(filename : str, data : any, format:str, dirname : str = None,):
#         print(format)
#         path = os.path.join(os.getcwd(), dirname, filename+format) or os.path.join(os.getcwd(), filename+format)
#         if data=='':
#             raise ValueError('not allowd to save whitespace')
        
#         with open(path, 'w', encoding='utf-8') as file:
#             file.write(data.decode())

#     @staticmethod
#     def read_file(Dir : str , filename : str, format : str = None):
#         absolute_path = os.path.join(os.getcwd(), Dir, filename)
#         try:

#             with open(absolute_path, mode='r', encoding='utf-8') as file:
#                 data : str= file.read()
#                 if data is not None:
#                     return data
            
#         except FileNotFoundError as e:
#             print('file not exists')
        
#         return None

# @dataclass
# class Key(object):
#     ___key_file_name = 'key'
#     __format = '.key'
    
  
#     def generate_fernet_key(self,*args,autosave : bool = None):
#         ''' return  pair che contiene fernet e key '''
#         key = Fernet.generate_key()
#         fernet = Fernet(key=key)
#         if autosave:
#             self.save_key(key=key)
#         return {'fernet':fernet, 'key':key}
    
#     def save_key(self, dirname : str = 'secret', key : bytes = None, force : bool = False):
#         path : str = os.path.join(os.getcwd(), 'env', 'Lib', dirname, self.___key_file_name +self.__format)
#         #save the key in a file with the content manager [with]
#         try:
#             if not os.path.exists(path):

#                 with open(path, 'w', encoding='utf-8') as file:
#                     if key is not None:
#                         file.write(key.decode())
#             else:
#                 if is_file_empty(Dir='env/Lib/secret', filename='key', format=self.__format):
#                     with open(path, 'w', encoding='utf-8') as file:
#                         if key is not None:
#                             file.write(key.decode())
#                 else:
#                     print(f' {path} already exists to overwrite it set force to True')

#         except TypeError as e:
#             print(str(e))
#         except FileNotFoundError as e:
#             pass
         
        
#     def load_key(self, dirname : str = 'secret') ->bytes:
#         Dir = 'env/Lib/secret'
#         key = IO.read_file(Dir=Dir, filename=self.___key_file_name, format=self.__format)
#         if key is not None:
#             print('importato!')
#             return key.encode()
#         return None
        
    
# def encrypt(data, key):
#     try:

#         data = data.encode() if isinstance(data, str) else data
#         fernet = Fernet(key)
#         token = fernet.encrypt(data)
#         return token
#     except AttributeError as e:
#         print(str(e))
      

       
        
# def decrypt(token, key):
#     token = token.encode() if isinstance(token, str) else token
#     fernet = Fernet(key)
#     data = fernet.decrypt(token=token)
#     print(data)
#     return data.decode()

# def is_data_is_encoded(data : any):
#     if data.startwith('gAA'):
#         return True
#     return False

# def is_file_empty(Dir, filename, format):
#     data = IO.read_file(Dir=Dir,filename=filename, format=format)
#     if data!='':
#         return False
#     return True
#     #     return False
    




        



