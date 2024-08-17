from flet import *

class CustomDropdown(Dropdown):
    def __init__(self, width, height, items:list = iter(range(1,30)), expand:bool=None, on_change = None):
    
        super().__init__(
            value='1',
            width=width,
            height=None,
            bgcolor='white',
            focused_bgcolor='white',
            icon_enabled_color=colors.PURPLE_700,
            focused_color='black',
            color='black',
            text_style=TextStyle(size=14, color='black'),
            border_radius=12,
            expand=None,
            on_change=on_change,
            options=[dropdown.Option(text = str(i)) for i in range(1,31)]
           
        )
    