import flet as ft
from flet import *
from dotenv import load_dotenv
import os
import threading
import asyncio

from app.pages.loading import Loading

dotenv_path = os.path.join(os.getcwd(), '.env')
print(load_dotenv(dotenv_path))

from app.utils.view import view_handler, change_route
from app.pages.login import Login



# async def install_dependesy():
#     await micropip.install('requests', verbose=True)
    
def main(page : Page):
    
    page.add(TextButton(text='ciaaao'))

    page.add(SafeArea(expand=True, content = Login(page)))
    page.on_route_change = lambda _ : change_route(page=page)

    page.bgcolor = colors.PURPLE_800 if page.platform.value =='windows'  else 'white'

    page.window_width,page.window_height = (650,740)
    if os.getenv('sub') is not None:
        page.go('auth')
        # loop = asyncio.get_running_loop()
        Loading(page).on_enter()
        
    else:
        page.go('/')
   
    

  
    
    
ft.app(target = main, assets_dir='assets', port=8000, host="0.0.0.0")
# ft.app(target =main, view=ft.AppView.WEB_BROWSER, port= 40400, host= '192.168.1.16',export_asgi_app=False)




                    