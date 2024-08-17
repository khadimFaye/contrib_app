from flet import *
import sys
import platform
from .dialog import ConfirmationDialog, Dialog
import requests
from dotenv import load_dotenv
import os

# from ..utils.encription import Key, decrypt
from ..utils.secure_storage import *
from .snackbar import CustomSnackbar
# # dotenv_path = os.path.join(os.getcwd(),'FRONTEND','resources','.env')
# load_dotenv(dotenv_path)


class contentCard(Card):
    # my_key = Key().load_key() or None
    def __init__(self, page, key:str, n:str, index, text = None, *args, traduction_text : str = 'aSDJFGUYWGHeuy r tuywetfuyasdtfuytsuy sdtuyf t usydtfuytweuyt uywefuysgdfuyftuy   teqwfiuypiuAODY IYT UYTSYUFT yagtgfuyatSUYFT BUY',STATUS :bool = False):
        #crea un istanza di page
        self._page = page
        self.argomento = key
        self.index = index
        self.n = n
        self.text = text
        self.dialog = ConfirmationDialog(title='avviso', callback=self.confirma)
        

        
        #definisci l'altezza minima é max
        self.mini_height = 150 if self._page.platform.value =='Windows' else 185
        self.max_height = 150*3
        # print(platform.system())

        #status widget 
        self.status = Container(
            border=Border(

                top=BorderSide(0.5, 'red'), 
                left = BorderSide(0.5, 'red'), 
                right=BorderSide(0.5, 'red'),
                bottom=BorderSide(0.5, 'red')) if not STATUS else  Border(

                top=BorderSide(0.5, 'green'), 
                left = BorderSide(0.5, 'green'), 
                right=BorderSide(0.5, 'green'),
                bottom=BorderSide(0.5, 'green')),

            padding = 4,
            border_radius=8,
            # bgcolor=colors.GREY,
            content=Row(
                [
                    Icon(name = icons.CANCEL if not STATUS else icons.CHECK_CIRCLE, color='red' if not STATUS else 'green', size = 14),
                    Text(value = 'non tradotto' if not STATUS else 'tradotto', color = colors.RED_700 if not STATUS else colors.GREEN_700, weight='w600', size = 13)]
            )
        )
        #request status 
        self.request_status = Container(
            border=Border(

                top=BorderSide(5.0, 'grey'), 
                left = BorderSide(5.0, 'grey'), 
                right=BorderSide(5.0, 'grey'),
                bottom=BorderSide(5.0, 'grey')),
           
            padding = 4,
            width =20,
            height = 20,
            border_radius=100,
            tooltip='nessuna richiesta fatta',
            data = 'grey'

            # bgcolor=colors.GREY,
           
        )

        #like button (optional)
        self.like_button = IconButton(
            icon = icons.THUMB_UP_ROUNDED,
            icon_color = 'black'
        )

        #avatar widget 
        self.avatar = CircleAvatar(
            content = Icon(name=icons.BOOK_ROUNDED)
        )
        #l'indeice della domnada ovvero il numero 
        self.indexLabel = Text(value = f'Domanda {index+1}', color=colors.BLACK87, weight='w600', size = 15)
        #collaple icon 
        self.collapse_icon = Row(
            expand=True,
            
            vertical_alignment=CrossAxisAlignment.END,
            alignment=MainAxisAlignment.START,
            controls=[IconButton(icon=icons.ARROW_DROP_DOWN, icon_size=40,on_click = self.extend)]
            )
        #label della domanda 
        self.questionLabel = Text(
            height=35,overflow=TextOverflow.FADE,
            value = text,color=colors.BLACK87,weight='w600')
        #traduction Label 
        self.traduction_label = TextField(
            value = traduction_text or 'n/f',
            multiline=True,
            text_style=TextStyle(
                size = 15,
                weight='w500',
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
            # focused_bgcolor= colors.with_opacity(0.70, 'black'),
            filled=True,
            # fill_color=colors.with_opacity(0.45, 'black')


        )
        
       
       
        
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
            on_click=self.showDialog)
        
        #content Column
        self.content_column = Column(
            visible=False,
            spacing = 2,
            controls = [
                #hint text
                Row(
                    alignment = MainAxisAlignment.START,
                    controls = [Container(),self.traduction_hint_text, Row(expand = True,alignment = MainAxisAlignment.END,controls=[self.edit_button, self.confirm_button])]
                ),

                Container(
                    padding =15,
                    expand = False,
                    border_radius = 8,
                    # bgcolor = colors.with_opacity(0.60,'black'),
                    content = self.traduction_label,
                ),
                Row(
                    key = 'actions',
                    controls = [
                        
                    ]
                )

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
                                self.avatar,self.indexLabel, self.collapse_icon]
                        ),


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

                        Row(
                            controls = [self.status, Container(margin=margin.only(left=20, right=20),border_radius = 5,height = 20,width=2,bgcolor = 'grey'),self.request_status]
                        )
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
    
    def extend(self, e):
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
        self.traduction_label.show_cursor = True
        self.traduction_label.bgcolor = colors.PURPLE_600

        self.update()

    def showDialog(self, e):
        self.content.content.controls.append(self.dialog)
        self.dialog.open = True
        self.update()
        # self.dialog.update()
        



        

    def confirma(self, e):  

        self.confirm_button.visible =False
        self.edit_button.visible = True
        self.traduction_label.read_only=True
        self.traduction_label.show_cursor = False
        self.traduction_label.bgcolor=colors.with_opacity(0.45, 'black')
        if e.control.text =='Si':
            self.send_translate_request()
        self.dialog.open = False
        self.update()
       
        self.update()
        
    def send_translate_request(self,*args):
        url = 'https://samaserver-51970f571916.herokuapp.com/send_translation_request'
        params = {"argomento":self.argomento,"value" :self.traduction_label.value,"n": self.n, "index": self.index,"question":self.text}
        token = get_token("mytoken", os.getenv('sub'))
        headers = {'Authorization' : f'Bearer {token}'}
        response = requests.post(url=url, params=params, headers=headers)
        if response.status_code ==200:
            self.set_snackbar('richiesta inviata!', 'green')
        else:
            self.set_snackbar('richiesta non inviata!', 'red')
      

    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.add(snackbar)
        self._page.open(snackbar)