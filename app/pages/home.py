from flet import *
from app.custums.cards import contentCard
from app.custums.dropdown import CustomDropdown
from app.custums.dialog import Dialog
from app.utils.functions import get_schede
from app.custums.snackbar import CustomSnackbar
from app.custums.navigationbar import menuBarButton



import requests
import os
import asyncio
import sys

from ..utils.secure_storage import *
import threading

dotenv_path = '.env'
load_dotenv(dotenv_path, override=True)



URLBASE = 'https://samaserver-51970f571916.herokuapp.com'
# URLBASE = 'http://127.0.0.1:3000'
ENDPOINT = '/content'
class Home(Container):
    __counter = 5
    __scheda_id = iter(range(1,30))
    # my_key = Key().load_key() or None
 
    
    def __init__(self,page, menuOpener):
        self._page = page
        self.dialog = Dialog(callback=self.select)
        self._page.add(self.dialog)
        
        self.reload_image = Image(src=f'/hotreload.gif', width=200, height=200)
        self.open_menu = menuOpener

        self.listview = ListView(
            spacing=8,
            controls=[Container(), Column(controls = [
                Row(alignment=MainAxisAlignment.CENTER, controls = [
                    Text(value = 'Seleziona un argomento',
                         size = 20, weight='w600',
                         color=colors.BLACK87)]),
                
                Row(alignment=MainAxisAlignment.CENTER, 
                    controls = [Image(src = '/load.gif', error_content=Icon(name=icons.IMAGE_NOT_SUPPORTED), filter_quality=FilterQuality.HIGH,)])
                    ]
                )   
            ]
        )

        #incoming notifications
        self.notifications = IconButton(
            icon = icons.NOTIFICATIONS,
            tooltip='box delle requeste'
        )
        self.inbox = IconButton(
            icon = icons.INBOX_ROUNDED,
            tooltip='box delle requeste'
        )

        self.custom_dropdown = CustomDropdown(
            width=100,
            height=90,
            on_change=self.verify_content,
            )
        
        self.notifications = IconButton(
            icon = icons.NOTIFICATIONS,
            icon_color = colors.GREY_500)
        
        self.profile = CircleAvatar(
            content=Icon(tooltip = self._page.client_storage.get('sub'),name = icons.PERSON))
        
        # self.username = Text(
        #     value = os.getenv('sub'),
        #     color = colors.BLACK54, 
        #     weight='w700', 
        #     size = 10, 
        #     expand=True,
        #     visible=True)
        
        self.badge = Badge(
            bgcolor = 'red',
            text = '3', 
            text_color='white',
            text_style=TextStyle(
                color=colors.WHITE, 
                weight='W400',),
                content =self.notifications if os.getenv('admin') in ['False', 'None'] else self.inbox)
        
        self.selected_arg = Row(
            expand=True,
            controls=[
                Text(
                    value = 'n/d',
                    width=180, 
                    height=21, 
                    overflow=TextOverflow.ELLIPSIS, 
                    color=colors.BLACK87, 
                    weight='w600')])
        
        self.selector_button = IconButton(
            icon=icons.ARROW_DROP_DOWN_CIRCLE, 
            icon_color=colors.BLUE_700,
            on_click=self.open_dialog)
        
        self.Argoment_selector= Container(
            expand=True,
            bgcolor='white',
            border_radius=12,
            padding = 10,
            tooltip=None,
            # height=50,
            border=Border(top=BorderSide(1, 'black'), left=BorderSide(1, 'black'), right=BorderSide(1, 'black'),bottom=BorderSide(1, 'black')),
            alignment=Alignment(x=50,y=50),

            
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Row(
                        alignment = CrossAxisAlignment.CENTER,
                        controls = [self.selected_arg, Container(),self.selector_button]
                        )
                        ]
        )
        )

        self.toolbar = Container(padding=padding.only(left=5, right = 10),content = Row(
            controls = [
                Row(
                    alignment=MainAxisAlignment.START,
                    controls = [IconButton(icon=icons.MENU_ROUNDED,icon_color=colors.BLACK87,on_click=self.open_menu)]),
                # Row(expand=True,alignment = MainAxisAlignment.START,controls = [
                #     Card(
                #         expand = 1,
                #         elevation = 0.80,
                #         color ='white',
                       
                #         content =TextField(
                #         expand = 2,
                #         # width = 250,
                #         hint_text='cerca..',
                #         border_radius=15,
                #         height = 45,
                #         fill_color='white',
                #         filled = True,
                #         border_width=2,
                #         border_color='white',
                #         visible = True if self._page.platform.value =='windows' else False,
                        
                       
                       
                #         prefix_icon='search'))
                #     ]),
                Container(expand=2,),
                Row(
                    expand = True,
                alignment=MainAxisAlignment.END,
                controls = [
                    self.badge,
                    self.profile,
                  
                    # Container()
                ])
                
            ]
        )
        )
        self.header = Row(
            alignment=MainAxisAlignment.CENTER,
            controls = [
               
                Row(expand=True,alignment = MainAxisAlignment.CENTER,controls = [Text(value='contribution platform'.title(), size=20, color = colors.BLACK87, weight = 'w700')])]
            )
        
 
    
        super().__init__(
            bgcolor=colors.with_opacity(0.90, 'white'),
            padding = 15,
            border_radius=12,
            # height=500,
            content=Column(
                scroll=ScrollMode.AUTO,
               
            controls=[
                self.toolbar,
                #RequestCard(page=self._page),
                # canvas.Canvas(
                #     expand = False,
                #     shapes =[
                #         canvas.Line(10,0,120,70)
                #     ]
                # ),
                Container(height=10),
                self.header,
                 Container(border_radius = 12, padding = 20,content=Column(controls = [
                    Text(value = 'La piattaforma permette di contribuire alla traduzione delle domande e altro >>'.capitalize(),size = 14, weight =FontWeight.NORMAL, color = colors.BLACK54),
                   
                ])),
                Container(height=10),

                Row(
                    
                    controls = [
                        self.Argoment_selector,
                        self.custom_dropdown,
                    ]),
                
                Row(alignment=MainAxisAlignment.START,controls = [Text(value = 'Risultati:',weight='w700',size=16, color = colors.BLACK54)]),
                Row(alignment=MainAxisAlignment.SPACE_EVENLY,
                    expand=False,
                       controls = [
                            Column(scroll=ScrollMode.HIDDEN,expand = True,controls = [self.listview]),
                        

                        ])],
            expand=True,

            ),
            expand=True
        )

    def is_selected(self, *args):
        if self.selected_arg.controls[-1].value!='n/d' and self.custom_dropdown.value is not None:
            self.Argoment_selector.tooltip =self.selected_arg.controls[0].value
            return True
        return False
    def clear(self, *args):
        self.listview.controls = []
        self.update()


    def get_scheda_from_db(self, key, n):
        try:
            
            #?argomento={key}&index={n}
            url = f'{URLBASE}{ENDPOINT}'
            # print('username', os.getenv('sub'))
            token = get_token(page=self._page, service_name='mytoken', username=self._page.client_storage.get('sub'))
            
        
            headers = {'Authorization' : f'Bearer {token}'}
            params = {'argomento':key, 'index':n}

            response = requests.get(url, headers=headers, params=params)
            if response.status_code==200:
                return response.json()
            
            elif response.status_code==401:
               return False

            elif response.status_code==204:
                return '0'
                
            return None
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            print(f'Errore: {e}')
        finally:
            if self.is_selected():
                self.clear()
            
            
    
    def verify_content(self, *args):
        
        key = self.selected_arg.controls[-1].value
        n = self.custom_dropdown.value
        scheda = self.get_scheda_from_db(key=key,n=n)
        if scheda is None:
            return None
        
        elif scheda ==False:
           
            self.listview.controls = [Icon(name=icons.WARNING_ROUNDED, color= 'red', size=100)]
            self.set_snackbar(message=f'stai per essere riindirzzato tra {self.__counter}', color=colors.YELLOW_800)
            self.update()
            self.start_countdown()
            return False
        
        elif scheda =='0':
           
            self.listview.controls = [
               Column(
                   spacing = 8,
                   controls = [
                       Container(),
                       Row(alignment=MainAxisAlignment.CENTER,controls = [Image(src = '/no_data.gif')],),
                       Container(),
                       Row(alignment=MainAxisAlignment.CENTER,controls = [Text(text_align=TextAlign.CENTER,value = f'indice selezionato [{n}] é maggiore delle schede disponibile per Argomento selezionato', weight='w500', color=colors.BLACK87)],),
                    ]
               )]
            # self.set_snackbar(message=f'indice selezionato [{n}] é maggiore delle schede disponibile per Argomento selezionato]', color=colors.YELLOW_800)
            self.update()
            
            return False
            
        self.showWidgets(scheda, key)
    
    def loading(self,*args):
        self.listview.controls = [self.reload_image]
        self.update()

            

    def showWidgets(self, scheda : list, key):
        controls = []
        self.loading()
        for i, j in enumerate(scheda):
            
            n = i+1
            domanda = j.get('domanda')
            actual_traduction = j.get('wolof')
            status = True if actual_traduction!='jappandi wull' else False
            card = contentCard(
            page = self._page, 
            n=str(n), 
            index=i,
            key=key,
            text=domanda, 
            STATUS=status,
            traduction_text=actual_traduction)
            controls.append(card)
            # self.listview.update()
            # self._page.update()
        time.sleep(0.9)
        self.listview.controls = controls
        self.update()

  

    def open_dialog(self, e):
        self._page.open(self.dialog)
        # self._page.update()
        # self.update()
    def select(self, e:ControlEvent):
        selected_value = e.control.text
        self.selected_arg.controls[0].value = selected_value
        self._page.close(self.dialog)
        self.verify_content()
        self.update()
    
    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.add(snackbar)
        self._page.open(snackbar)
    
    def start_countdown(self, *args):
        def coundown():
            self.__counter -= 1
            if self.__counter >0:
                time.sleep(1.0)
                print(self.__counter)
                return coundown()
            if self.__counter==0:
                self._page.go('login')
        threading.Thread(target=coundown).start()
        
        