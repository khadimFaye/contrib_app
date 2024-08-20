from flet import *
# from ..custums.request_card import RequestCard
# from ..utils.encription import IO, encrypt, decrypt, Key
from ..utils.secure_storage import *
import requests
import time
from datetime import datetime

# from dotenv import load_dotenv
# from ..custums.snackbar import CustomSnackbar
# from app.custums.navigationbar import menuBarButton

# dotenv_path = os.path.join(os.getcwd(),'FRONTEND','resources','.env')
# load_dotenv(dotenv_path)

# URL_base = 'https://samaserver-51970f571916.herokuapp.com'
# # URL_base = 'http://127.0.0.1:3000'
# ENDPOINT = "fetch_requests"

class LogsPage(Container):
    # __key__ = Key().load_key() or Key().generate_fernet_key(autosave=True)
    __flag = 0
    def __init__(self, page, callback):
        self._page = page
       
        self.listview = ListView(spacing=8, controls=[self.excpetion_illustration(message='Nessuna attivita')])
        self.list_users = GridView(runs_count=1,spacing=8,)
        self.menu_opener = callback
        self.navbar =IconButton(icon = icons.ARROW_BACK, icon_color=colors.BLACK87, on_click=lambda e :self.menu_opener(e))

        super().__init__(
            bgcolor=colors.with_opacity(0.95, 'white'),
            padding = 15,
            border_radius=12,
            # height=500,
            content=Column(
                
                scroll=ScrollMode.AUTO,
                 controls=[
                    Container(
                       expand = False,
                        padding = 5,
                        bgcolor = 'white',
                        content=Row(
                                controls=[
                                Row(
                                    
                                    alignment=MainAxisAlignment.START, 
                                    controls = [self.navbar],
                                    
                                ),
                                
                                Row(
                                    expand = True,
                                    alignment=MainAxisAlignment.CENTER, 
                                        controls = [
                                            
                                            Icon(
                                                name = icons.HISTORY,
                                                color=colors.BLUE_700,
                                            ),
                                            Text(
                                                value = 'registri'.title(), 
                                                weight='w600', 
                                                size = 20,
                                                color=colors.BLACK87),
                                            
                                            ]),
                                    
                                ]
                        )
                    ),
            #counter
            Divider(),
            Container(),
            
            
            self.listview
            #divider


            #listview
          
          
           
                ]
            ),
        expand=True,
        )
        
    
    
    @property
    def flag(self):
        return self._flag
    @flag.setter
    def flag(self, value:bool):
        self._flag = value
        
    def clear(self,*args):
        self.listview.controls=[]
        self.update()
    
    def check_if_childs_exists(self, *args):
        if self.listview.controls!=[]:
            self.clear()
        else:
            print('children')
          
       

    def check_activity(self, *args):
        pass
      
        
        

  
    def excpetion_illustration(self,message:str ='Nessuna attivita!', image: Control = Icon(name=icons.INBOX_ROUNDED, size=30, color='grey')):
        
        return Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=False,
            controls=[
                image,
                Text(value=message, color = colors.BLACK87, text_align=TextAlign.CENTER, weight='w500')]
            )
    
    def check_platform(self,*args):
        if self._page.platform.value == 'windows':
            return True
        return False
        
# <