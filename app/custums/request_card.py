from flet import *
import os
import requests
# from flet.security import encrypt, decrypt
from ..utils.secure_storage import *
from dotenv import load_dotenv
from .snackbar import CustomSnackbar
from app.custums.log_template import admin_log_template

dotenv_path ='.env'
load_dotenv(dotenv_path)

Url_base = 'https://samaserver-51970f571916.herokuapp.com'
Endpoint = 'translation_aprovation'

class RequestCard(Card):
    def __init__(self, page, refresh, request_id, username : str ,argomento, index, questionIndex:int, badge = None, question='questo é una prova ?', incoming_traduction_text:str = None , traduction_text : str = 'aSDJFGUYWGHeuy  BUY',timestamp=123.23445, STATUS:bool = False):
        #crea un istanza di page
        self._page = page
        self.argomento = argomento
        self.index = index
        self.request_id = request_id
        self.questionIndex = questionIndex
        self.question = question
        self.refresh = refresh
        self.badge = badge
        #definisci l'altezza minima é max
        self.mini_height = 150 if self._page.platform.value =='Windows' else 190
        self.max_height = 150*3
        
        #accpet or decline buttons
        self.accept_button = TextButton(
            text = 'approva',
            style=ButtonStyle(color='green'),
            icon = icons.CHECK_CIRCLE_OUTLINE, 
            icon_color=colors.GREEN_400,
            
            tooltip='aprova',
            on_click = self.approve_request)
        
        self.decline_button = TextButton(
            text = 'rifiuta',
            style=ButtonStyle(color='red'),
            icon = icons.CANCEL_ROUNDED, 
            icon_color=colors.RED_400,
          
            tooltip='rifiuta',
            on_click = self.delet_request)
        

        #status widget 
        self.status = Container(
            # border=Border(
            #     top=BorderSide(0.5, 'red'), 
            #     left = BorderSide(0.5, 'red'), 
            #     right=BorderSide(0.5, 'red'),
            #     bottom=BorderSide(0.5, 'red')) if not STATUS else Border(

            #     top=BorderSide(0.5, 'green'), 
            #     left = BorderSide(0.5, 'green'), 
            #     right=BorderSide(0.5, 'green'),
            #     bottom=BorderSide(0.5, 'green')),
            bgcolor=colors.GREY_500,

            padding = 4,
            border_radius=8,
            # bgcolor=colors.GREY,
            content=Row(
                [
                    # Icon(name = icons.CANCEL if not STATUS else icons.CHECK_CIRCLE, color='red' if not STATUS else 'green', size = 14),
                    Text(value = 'da approvare' if not STATUS else 'approvato', color = colors.WHITE60 if not STATUS else colors.GREEN_700, weight='w600', size = 13)]
            )
        )
       
        #like button (optional)
        self.like_button = IconButton(
            icon = icons.THUMB_UP_ROUNDED,
            icon_color = 'black'
        )

        #avatar widget 
        self.avatar = CircleAvatar(
            content = Icon(name=icons.PERSON)
        )
        #l'indeice della domnada ovvero il numero 
        self.username = Text(value = username, color=colors.BLACK87, weight='w600', size = 15)
        #collaple icon 
        self.time = Text(value = timestamp, color=colors.BLACK87, weight='w400', size = 10)
       
        self.collapse_icon = Row(
            expand=True,
            
            vertical_alignment=CrossAxisAlignment.END,
            alignment=MainAxisAlignment.START,
            controls=[IconButton(icon=icons.ARROW_DROP_DOWN, icon_size=40,on_click = self.extend)]
            )
        
        #label della domanda 
        self.questionLabel = Text(
            height=35,overflow=TextOverflow.FADE,
            value =self.question ,color=colors.BLACK87,weight='w600')
        
        #traduction Label 
        self.traduction_label = TextField(
            value = traduction_text or 'n/f',
            multiline=True,
            text_style=TextStyle(
                size = 13,
                weight='w400',
                color = 'white', 
                ),
            keyboard_type=KeyboardType.TEXT,
            read_only=True,
            show_cursor=True,
            expand = True,
            border_radius=10,
            border_width=0,
            focused_border_width=None,
            bgcolor=colors.with_opacity(0.45, 'black'),
            focused_bgcolor= colors.with_opacity(0.70, 'black'),
            filled=True,
            # fill_color=colors.with_opacity(0.45, 'black')


        )
        
        #  Text(
        #     value = traduction or 'n/d', 
        #     color = colors.WHITE, 
        #     weight='w500', size = 13 )
        
        self.traduction_hint_text = Text(
            value = 'traduzione wolof :'.capitalize() , 
            color = colors.BLACK87, 
            weight='w700', size = 15 )
        
        #edit button
        self.edit_button = IconButton(
            icon = icons.EDIT_NOTE, 
            icon_color=colors.BLUE_600,
            icon_size=28,
            tooltip='modifica',
            on_click = self.traduci)
        
        #confirmation button
        self.confirm_button = IconButton(
            icon = icons.CHECK_CIRCLE_ROUNDED, 
            icon_color=colors.GREEN_600,
            icon_size=30,
            visible=False,
            tooltip='confirma',
            on_click=self.confirma)
        
        #content Column
        self.content_column = Column(
            visible=False,
            spacing = 2,
            controls = [
                #hint text
                # Row(
                #     alignment = MainAxisAlignment.START,
                #     controls = [Container(),Row(expand = True,alignment = MainAxisAlignment.END,controls=[self.edit_button, self.confirm_button])]
                # ),
                Row(
                    spacing=-5,
                    expand = False,
                    controls=[
                        Container(
                        padding =5,
                        expand = True,
                        border_radius = 8,
                        # bgcolor = colors.with_opacity(0.60,'black'),
                        content = self.traduction_label,
                        ),
                    self.edit_button, self.confirm_button]
                    ),
                    
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    key = 'actions',
                    controls = [
                        self.accept_button,
                        self.decline_button
                    ]
                ),

            ]
        )


        #il container delle widget 
        self.container = Container(
                animate_size=Animation(duration=220,curve=AnimationCurve.EASE_IN_OUT_CUBIC),
                padding=10,
                height=self.mini_height,
                expand = True,
                adaptive=True,
                # on_click=self.extend,
                content = Column(
                    spacing=8,
                    adaptive=True,
                    controls = [
                        
                      
                        Row(
                            controls = [
                                self.avatar,
                                Column(spacing=-5,controls = [self.username,self.time]), 
                                self.collapse_icon]
                        ),
                        Divider(height = 5),

                        #question container
                        Row(

                            controls = [
                                Container(
                                padding = padding.only(left = 10, right = 10),
                                expand=True,
                                content = Column(tight=True,alignment=MainAxisAlignment.CENTER,controls=[self.questionLabel])
                        )]
                        ),
                        #space
                        Container(),

                        #traduction Column
                        self.content_column
                        ,

                        # Row(
                        #     controls = [Container(margin=margin.only(left=20, right=20),border_radius = 5,height = 20,width=2,bgcolor = 'grey')]
                        # ),

                        #space
                        Container(),
                    ]
                ),
                #Row(alignment = MainAxisAlignment.END, expand = True,controls = [self.like_button])
            data=self.mini_height
        )
        super().__init__(
            elevation=4,
            color=colors.with_opacity(0.98, 'white'),
            surface_tint_color=colors.PURPLE_100,
            expand=False,
            content=self.container
            ,
        data=self.mini_height
        )
    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.add(snackbar)
        self._page.open(snackbar)

    def extend(self, *args):
        if self.container.data<self.max_height:
            #imposta l'animazione dell ingrandimento 
            self.container.animate_size = Animation(260, curve=AnimationCurve.FAST_OUT_SLOWIN)
            #setta l'altezza del container a None in modo che si adatti ai suoi widget
            self.container.height = None
            #cambia il valore della data e metti l altezza massima
            self.container.data = self.max_height
            #setta anche l altezza della questionLabel to None
            self.questionLabel.height = None
            #rendi visibile la colonna dei widgets
            self.content_column.visible =True
            self.collapse_icon.controls[-1].icon=icons.ARROW_DROP_UP
        else:
            self.container.animate_size = Animation(200, curve=AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
            self.container.height = self.mini_height
            self.container.data = self.mini_height
            self.questionLabel.height = 35
            self.collapse_icon.controls[-1].icon=icons.ARROW_DROP_DOWN
            self.content_column.visible =False
        self.update()

    def traduci(self, e):
        e.control.visible =False
        self.confirm_button.visible = True
        self.traduction_label.read_only=False
        
        self.update()

    def confirma(self, e):
        e.control.visible =False
        self.edit_button.visible = True
        self.traduction_label.read_only=True
        self.update()
        
    def approve_request(self, e):
 
        try:
            


            url = f'{Url_base}/{Endpoint}'
            headers = {'Authorization':f"Bearer {get_token(self._page, 'mytoken', self._page.client_storage.get('sub'))}"}
            params = {'argomento' : self.argomento, 'index' : self.index, 'ID' : self.questionIndex, 'value':self.traduction_label.value}
            response = requests.post(url=url, headers=headers, params=params)
            if response.status_code==200:
                self.color = 'green'
                self.extend()
                
                self.tooltip = 'approvato'
                self.update()
                self.delet_request(e)
                self.send_log(message='ha approvato la richiesta di: ')
            

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout) as e:
            print('connection error ', str(e))
        except Exception as e:
            print('error ', str(e))
            self.set_snackbar(message='qualcosa é andato storto :( {str(e)}', color='red')
       
    def delet_request(self, e):
        try:
            
            url = 'https://samaserver-51970f571916.herokuapp.com/delete_requests'
                
            headers = {'Authorization':f"Bearer {get_token(self.page, 'mytoken', self._page.client_storage.get('sub'))}"}
            params = {'request_id' : self.request_id}
            response = requests.post(url=url, headers=headers, params=params)
            if response.status_code==200:
                if e.control.text=='approva':
                    self.color = 'green'
                    self.extend()
            
                    self.set_snackbar(message='richiesta processata!', color='green')
                        
                else:
                    self.set_snackbar(message='richiesta eliminata', color='red')
            else:
                self.set_snackbar(message='qualcosa é andato storto :(', color='red')
                
        except Exception as e:
            print('error ', str(e))
            self.set_snackbar(message=f'qualcosa é andato storto :( {str(e)}', color='red')
        finally:
            if e.control.text=='rifiuta':
                self.send_log(message='ha rifiutato la richiesta di: ')
            # print('finally')
            self.refresh()
            
            
    def send_log(self, message, *args):
        self._page.pubsub.send_all(
            admin_log_template(
                admin=self._page.client_storage.get('sub'),
                user=self.username.value,
                detail=message
                
            ))
      
        self.badge.text = len(self._page.data['logs'])
        self.update()
        
            


