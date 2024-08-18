
import flet as ft
from flet import View, colors

from ..pages.main_page import MainApp
from ..pages.login import Login
from ..custums.navigationbar import Navbar
from ..custums.navigationRail import Navrail
from ..pages.loading import Loading
from ..pages.signup import Signup

def view_handler(page):
    home = MainApp(page)
    print(page.platform.value)
    

    return {
        
        '/' : View(
            route='/',
            controls= [ft.SafeArea(expand=True,content=home)],
            bgcolor=colors.PURPLE_800 if page.platform.value =='windows' else 'white',
            ),

        'auth' : View(
            route='/',
            controls= [Loading(page)],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           
            bgcolor=colors.PURPLE_800 if page.platform.value =='windows' else 'white',
            ),

        'login' : View(
            route='/',
            
            controls= [ft.Card(color = 'white',surface_tint_color='white',content = Login(page))],
            bgcolor= colors.PURPLE_800 if page.platform.value =='windows'  else 'white',
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
          
    
            
            ),

        'signup' : View(
            route='/',
            
            controls= [ft.Card(color = 'white',surface_tint_color='white',content = Signup(page))],
            bgcolor=ft.colors.PURPLE_800,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          
    
            
            )

        
    }
 


def change_route(page,handler=view_handler):
    # print(page.route) 
    page.views.clear() 
    page.views.append(handler(page)[page.route])
    page.update()
