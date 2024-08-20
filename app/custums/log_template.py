from flet import *
from flet import colors
from datetime import datetime

class log_template(Container):
    def __init__(self, autore:str =None , argomento:str = None, detail:str='ha fatto una richiesta'):
        super().__init__(
            bgcolor='white',
            border=Border(left=BorderSide(width=3, color='grey')),
            border_radius=12,
            height=100,
            
            padding = 10,
            
            content= Column(
                controls = [
                    #autore container
                    Row(
                        controls = [Column([Container(padding = 5, border_radius=10, bgcolor=colors.random_color(), content=Row([Icon(name = icons.PERSON, color='white'), Text(value=autore, color='white'), ])),]),  Container(width=3,height=30,bgcolor='grey'), Text(expand=False, value = detail, text_align=TextAlign.LEFT, color = colors.BLACK87, weight='w400')]
                    ),
                    # Divider(),
                    #deatil container
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls = [Container(padding=10, content=Text(expand=True, value = datetime.now().strftime("%H:%M"), text_align=TextAlign.LEFT, color = colors.BLUE_400))]
                    ) 
                ]
            )
        )
    
class admin_log_template(Container):
    def __init__(self, admin:str =None , user:str = None, detail:str='ha approva la richiesta fatta da : '):
        super().__init__(
            bgcolor='white',
            border=Border(left=BorderSide(width=3, color='grey')),
            border_radius=12,
            height=100,
            
            padding = 10,
            
            content= Column(
                controls = [
                    #autore container
                    Row(
                        controls = [Column([Container(padding = 5, border_radius=5, bgcolor=colors.GREEN_200, content=Row([Icon(name = icons.PERSON, color='white'), Text(value=admin, color='white'), ])),]),  Container(width=3,height=30,bgcolor='grey'), Text(expand=True, spans=[TextSpan(text = detail), TextSpan(text=user.upper(), style=TextStyle(weight='w800', color=colors.random_color()))], text_align=TextAlign.LEFT, color = colors.BLACK87, weight='w500')]
                    ),
                    # Divider(),
                    #deatil container
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls = [Container(padding=10, content=Text(expand=True, value = datetime.now().strftime("%H:%M"), text_align=TextAlign.LEFT, color = colors.GREEN_200))]
                    ) 
                ]
            )
        )
    
            
