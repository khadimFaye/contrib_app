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



# async def install_dependesy):
#     await micropip.install('requests', verbose=True)
class log_template(Card):
    def __init__(self, autore:str =None , argomento:str = None, detail:str='ha fatto una richiesta'):
        super().__init__(
            color='white',
            surface_tint_color='white',
            content= Container(
                padding = 10,
                content = Column(
                controls = [
                    #autore container
                    Row(
                        controls = [Container(border_radius=12, bgcolor=colors.PURPLE_600, content=Row([Icon(name = icons.PERSON, color='white'), Text(value=autore, color='white')]))]
                    ),
                    Divider(),
                    #deatil container
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls = [Container(padding=10, content=Text(expand=True, value = detail, text_align=TextAlign.LEFT, color = colors.BLACK87))]
                    ) 
                ]
            )
        )
    )
    
def main(page : Page):

    page.add(TextButton(text='ciaaao'))
    page.theme_mode = 'light'
    page.add(SafeArea(expand=True, content = Login(page)))
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

