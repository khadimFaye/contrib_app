import flet as ft
from flet import(
    TextField,
    Row,
    Column,
    Container,
    Card,

    TextButton,
    Text,
    ElevatedButton,
    IconButton,
    FilledButton,
    FilledTonalButton,

    colors,
    icons,
    padding,
    border_radius,
    border,

)

import os
import sys
import platform
import threading
import asyncio
import json
from dotenv import set_key, load_dotenv
import requests
import string

from ..utils.functions import change_view
# from ..utils.encription import IO, decrypt, encrypt, Key
from ..utils.secure_storage import *
from jose import ExpiredSignatureError, JWTError
# from fastapi import HTTPException, status
from ..custums.snackbar import CustomSnackbar

dotenv_path = '.env'
load_dotenv(dotenv_path)
print(dotenv_path)

URL_BASE = 'https://samaserver-51970f571916.herokuapp.com'
# URL_BASE = 'http://127.0.0.1:3000'
ENDPOINT = '/signup'



class Signup(Container):
    # my_key = Key().load_key() or Key().generate_fernet_key(autosave=True)
    def __init__(self,page):
        super().__init__(padding = padding.only(left =20, right=20),margin=ft.margin.all(10.0),alignment=ft.alignment.center,blur=ft.Blur(sigma_x=0.5,sigma_y=0.5),border_radius = 12)
        self._page = page
       
        self.email = TextField(
            hint_text='email...',
            text_style=ft.TextStyle(color = ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.BLACK45),
            height = 85,
            width= 300,
            focused_border_width=4,
            border_radius=ft.border_radius.all(3),
            border_color=colors.PURPLE_700,
            focused_border_color=colors.PURPLE_900,
            bgcolor=colors.WHITE,
            max_length=40,
            helper_text='user@gmail.com',
            filled=True,

        )
        self.name = TextField(
            hint_text='nome...',
            text_style=ft.TextStyle(color = ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.BLACK45),
            height = 60,
            width=300,
            border_radius=ft.border_radius.all(3),
            focused_border_width=4,
            border_color=colors.PURPLE_700,
            focused_border_color=colors.PURPLE_900,
            bgcolor=colors.WHITE,
            password=False,
            enable_suggestions=True,
          


        )
        self.password = TextField(
            hint_text='password...',
            text_style=ft.TextStyle(color = ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.BLACK45),
            height = 60,
            width=300,
            border_radius=ft.border_radius.all(3),
            focused_border_width=4,
            border_color=colors.PURPLE_700,
            focused_border_color=colors.PURPLE_900,
            bgcolor=colors.WHITE,
            password=True,
            enable_suggestions=True,
          


        )

        self.sumbit_button = ft.FilledButton(
            text='invia'.title(), 
            style=ft.ButtonStyle(
                bgcolor = ft.colors.PURPLE_600, 
                color='white'
                ),
            on_click=self.send_access_request)
        
        self.content = Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand = True,
            spacing = 5,
            controls = [
                Row(visible= False if self._page.platform.value!='windows' else True ,expand = True,controls = [ft.Image(expand=True,src=os.path.join(os.getcwd(),'assets','log_vector.jpg'),width = 500, height = 600, fit=ft. ImageFit.CONTAIN),]),
                #welcome text
                Container(width = 10,expand = False),
                Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand =True,spacing = 10,controls=[
                    Container(),
                    Text(value='Registrati :)'.capitalize(),size = 20, color=ft.colors.BLACK87, weight = ft.FontWeight.BOLD),
                    Text(value = 'Nota : L\'email fornito verra utilizzato solo a scopo informativo.'.capitalize(),weight='w500',size = 14, color = ft.colors.BLACK54, ),
                    #space
                    Container(height = 20),
                    Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing = 8,
                        controls = [
                            self.name,
                            self.email, 
                            self.password,
                            Container(height = 10,), 
                            Row(
                                alignment=ft.MainAxisAlignment.CENTER if self._page.platform !='windows' else None,
                                controls = [
                                    self.sumbit_button, 
                                    ft.TextButton(
                                        text='login'.title(),
                                        on_click =lambda _:self._page.go('login'),
                                        style=ft.ButtonStyle(
                                            color = ft.colors.BLACK38, 
                                            bgcolor = ft.colors.WHITE))])])
                    ]),
                    
            ]
        )

    def Animate(self, event ):
        event.control.scale = 2
        event.control.scale = 1
        self.update()

    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.add(snackbar)
        self._page.open(snackbar)

    def input_validator(self,*args):
        ponctuation = string.punctuation
        letters = string.ascii_uppercase
        white_space = string.whitespace
        
        if not all([self.email.value, self.password.value, self.name.value]):
            self.set_snackbar(message='impossibile effettuare la richiesta con un campo vuoto!', color='red')
            raise ValueError()
        
        elif '@' not in list(self.email.value):
            self.set_snackbar(message=f'Email invalido prego ricontrolla', color='red')
            raise ValueError()
        elif self.email.value.lower().split('@')[1] not in ['gmail.com','hotmail.com', 'icloud.com']:
            self.set_snackbar(message=f' metti un provider valido [gmail.com - hotmail.com - icloud.com]', color='red')
            raise ValueError()
            
         
        elif self.password.value is None or len(self.password.value)<8:
            self.set_snackbar(message=f' il password deve essere lungo almeno 8 carratteri deve contenere ({ponctuation})', color='red')
            raise ValueError()
        
        elif self.name.value is None or self.email.value is None:
            self.set_snackbar(message=f'nome o email é vuoto controlla per favore', color='red')
            raise ValueError()
        
        
        elif self.password.value is not None:
            for substring in self.password.value:
                if substring == white_space:

                    self.set_snackbar(message=f' il password non deve contenere spazi', color='red')
                    raise ValueError()
        # elif  any(substring in ponctuation for substring in self.password.value) ==False:
        #     print('haha')
        #     self.set_snackbar(message=f' il password deve essere contenere uno di questi carratteri ({ponctuation})', color='red')
        #     raise ValueError()
                
            # self.set_snackbar(message=f' il password deve essere lungo almeno 8 carratteri deve contenere ({ponctuation})', color='red')
            # raise ValueError()
        

    def send_access_request(self, *args):
        self.input_validator()
       

        url = f'{URL_BASE}{ENDPOINT}'
    

        user_form = {'username' :self.name.value, 'email' : self.email.value, 'hashed_password' : self.password.value, 'disablited':False, 'admin' : False}
        headers = {'Content-Type' : 'application/json'}
        user_json = json.dumps(user_form)
        try:
            
            response = requests.post(url=url, data=user_json, headers=headers)
            if response.status_code==200:
                self.set_snackbar(message='richiesta inviata con successo!', color='green')
                    # self._page.go('/')
            
            elif response.status_code==226:
                self.set_snackbar(message='esiste un account legato a questo email!', color='red')
                # self.set_snackbar(message='hai loggato con successo!', color='green')
            
                # return response.json()['user']
            
       
        except Exception as e:
            self.set_snackbar(message='connessione assente {alert : Verifica la tua connesione}', color='red')
            
     
    
    def on_enter(self,*args):
      
        try:

            username = os.getenv('sub')
            token = get_token('mytoken', username)
            payload = jwt.decode(token = token, key=os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])

            activce_user = payload.get('sub')
            if activce_user is None:
                raise ValueError('sessione terminata fai il login di nuovo')
            #     raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )


                # response = requests.post(url=url,)
        except ExpiredSignatureError as e:
            raise ValueError('sessione terminata fai il login di nuovo')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )
        except JWTError:
            raise ValueError('sessione terminata fai il login di nuovo')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )
        except AttributeError:
            self.set_snackbar(message='sessione terminata fai il login di nuovo:(', color='red')
            raise ValueError('sessione terminata fai il login di nuovo')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )
            
       
        self.set_snackbar(message='hai loggato con successo!', color='green')
        self._page.go('/')

    def start(self, *args):
        thread = threading.Thread(target=self.on_enter)
        thread.start()

            
