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
# import json
from dotenv import set_key, load_dotenv
import requests
from ..utils.functions import change_view
# from ..utils.encription import IO, decrypt, encrypt, Key
from ..utils.secure_storage import *
from jose import ExpiredSignatureError, JWTError
# from fastapi import HTTPException, status
from ..custums.snackbar import CustomSnackbar

dotenv_path = '.env'
load_dotenv(dotenv_path, override=True)


URL_BASE = 'https://samaserver-51970f571916.herokuapp.com'
# URL_BASE = 'http://127.0.0.1:3000'
ENDPOINT = 'token'



class Login(Container):
    # my_key = Key().load_key() or Key().generate_fernet_key(autosave=True)
    def __init__(self,page):
        super().__init__(padding = padding.only(left =20, right=20),margin=ft.margin.all(10.0),alignment=ft.alignment.center,blur=ft.Blur(sigma_x=0.5,sigma_y=0.5),border_radius = 12)
        self._page = page
       
        self.username = TextField(
            hint_text='username...',
            text_style=ft.TextStyle(color = ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.BLACK45),
            height = 85,
            width= 300,
            focused_border_width=4,
            border_radius=ft.border_radius.all(3),
            border_color=colors.PURPLE_700,
            focused_border_color=colors.PURPLE_900,
            bgcolor=colors.WHITE,
            max_length=30,
            helper_text='user@gmail.com',
            filled=True,

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
            password=True

        )

        self.sumbit_button = ft.FilledButton(text='dugal'.title(), style=ft.ButtonStyle(bgcolor = ft.colors.PURPLE_500, color='white'),on_click=self.authenticate)
        self.content = Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand = True,
            spacing = 5,
            controls = [
                Row(
                    visible= False if self._page.platform.value!='windows' else True ,
                    expand = True,controls = [ft.Image(expand=True,src='/log_vector.jpg',width = 500, height = 600, fit=ft. ImageFit.CONTAIN),]),
                #welcome text
                Container(width = 10,expand = False),
                Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand =True,spacing = 10,controls=[
                    Container(),
                    Text(value='dala ak jam :)'.title(),size = 20, color=ft.colors.BLACK87, weight = ft.FontWeight.BOLD),
                    Text(value = 'nguir mana dugu ci platform bi dugeul ak sa compte'.title(),size = 14, color = ft.colors.BLACK54, ),
                    #space
                    Container(height = 20),
                    Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing = 1,
                        controls = [
                            self.username,
                            self.password, 
                            Container(height = 10,), 
                            Row(
                                alignment=ft.MainAxisAlignment.CENTER if self._page.platform !='windows' else None,
                                controls = [
                                    self.sumbit_button, 
                                    ft.TextButton(
                                        text='scriviti'.title(),
                                        on_click = lambda _ :self._page.go('signup'),
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

    def authenticate(self, *args):
        if self.username.value is None or self.password.value is None:
            self.set_snackbar(message='** campo vuoto', color='red')
            raise ValueError()
        

        url = f'{URL_BASE}/{ENDPOINT}'
        data = {'username' :self.username.value, 'password' : self.password.value}
        response = requests.post(url=url, data=data)
        if response.status_code==200:
           
            user = response.json()['user']
            save_token(service_name='mytoken', username=user['username'], token=response.json()['access_token'])
            set_key(dotenv_path, 'sub', user.get('username'))
            set_key(dotenv_path, 'admin', str(user.get('admin')))

            self.set_snackbar(message='hai loggato con successo!', color='green')
            load_dotenv(dotenv_path, override=True)
            self._page.go('/')
            # return response.json()['user']
        
        else:
            self.set_snackbar(message='credenziali invalidi:( ', color='red')
     
    
