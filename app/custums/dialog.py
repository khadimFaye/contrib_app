from flet import *
from app.utils.functions import get_args


class Dialog(AlertDialog):
    def __init__(self, title = None, content=None, buttons=None, callback = None):
        self.callback = callback
        self.lista_args = get_args()
        super().__init__(
            title=Text(value = title or 'argomenti'),
            elevation=10,
            bgcolor='white',
            surface_tint_color = colors.BLACK12,
            actions=buttons, 
            open=False,
            modal=False,
            content=Container(
                padding=10,
                expand=False,
                height = 250,
                content=Column(
                    controls = [
                        ListView(
                            height = 200,
                            controls=[
                               Card(color='white', content = TextButton(text = arg, on_click=self.callback or None, style=ButtonStyle(color = 'black')))  for arg in self.lista_args
                            ]

                        )
                    ]

                )
            ), 
        )

class ConfirmationDialog(AlertDialog):
    def __init__(self, title = None, content=None, callback = None):
        self.callback = callback
        
        super().__init__(
            title=Text(value = title or 'argomenti'), 
            bgcolor='white',
            actions=[
                TextButton(text='Si',on_click= callback ,style=ButtonStyle(color=colors.BLACK87)),
                TextButton(text='No',on_click= callback ,style=ButtonStyle(color=colors.BLACK87))
            ],
        
            modal=False,
            content=Container(
                padding=10,
                # 
                # height = 250,
                content=Text('sei sicuro di voler ocnfermare?', color=colors.BLACK87)))
    def select(self, e ):
        if self.callback is not None:
            self.callback(e) 