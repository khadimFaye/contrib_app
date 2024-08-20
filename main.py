import flet as ft
from flet import *
from dotenv import load_dotenv
import os
import threading
import asyncio
from app.pages.logs_page import LogsPage


from app.pages.loading import Loading

dotenv_path = os.path.join(os.getcwd(), '.env')
print(load_dotenv(dotenv_path))

from app.utils.view import view_handler, change_route
from app.pages.login import Login
from app.pages.main_page import MainApp



# async def install_dependesy):
#     await micropip.install('requests', verbose=True)

    
def main(page : Page):
    
    page.data = {'control' : None, 'logs' : []}
    def on_message(message):
       page.data['logs'].append(message)
       logs_storage = page.data['logs']
       page.client_storage.set('logs', logs_storage)
       page.update()
       
    page.pubsub.subscribe(on_message)
       
       
       
    page.theme_mode = 'light'
    # page.add(SafeArea(expand=True, content = Login(page)))
    page.on_route_change = lambda _ : change_route(page=page)
  

    page.bgcolor = colors.PURPLE_800 if page.platform.value =='windows'  else 'white'

    page.window.width,page.window.height = (650,740)
    
    if page.client_storage.get('sub') is not None:
        print('utent', page.client_storage.get('sub'))
        page.go('auth')
        # loop = asyncio.get_running_loop()
        Loading(page).on_enter()
        
    else:
        page.go('login')
   
    

  
    
    
ft.app(target = main, assets_dir='assets', view=AppView.WEB_BROWSER)
# ft.app(target = main, assets_dir='assets')
# ft.app(target =main, view=ft.AppView.WEB_BROWSER, port= 40400, host= '192.168.1.16',export_asgi_app=False)

