from flet import *

class CustomSnackbar(SnackBar):
    def __init__(self,  message:str, icon_color = None, bgcolor = None, page=None):
        super().__init__(
            content=Container(
                content=Row(
                    controls = [
                        Icon(name = icons.WARNING_ROUNDED, color=icon_color),
                        Text(expand=True,value=message, size=14, weight='w600', color='white'),

                    ]
                )
            ),
            action='Capito',
            bgcolor=bgcolor
        )