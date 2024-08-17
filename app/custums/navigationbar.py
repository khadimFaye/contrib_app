from flet import *

class Navbar(NavigationBar):
    __destinations = [
        {
            'icon': icons.HOME_OUTLINED,
            'label': 'home',
            'selected_icon': icons.HOME_FILLED
        },
        {
            'icon': icons.HISTORY_OUTLINED,
            'label': 'logs',
            'selected_icon': icons.HISTORY
        },
       
        {
            'icon': icons.ADMIN_PANEL_SETTINGS_OUTLINED,
            'label': 'admin',
            'selected_icon': icons.ADMIN_PANEL_SETTINGS
        },
        
        {
            'icon': icons.SETTINGS_OUTLINED,
            'label': 'impostazioni',
            'selected_icon': icons.SETTINGS
        },
            ]

    def __init__(self, callback = None, visible : bool = None):
        self.callback = callback
        super().__init__(
            selected_index=0,
            bgcolor=colors.PURPLE_800,
            visible=visible,
            destinations=[
                NavigationDestination(
                    icon=destination['icon'],
                    selected_icon=destination['selected_icon'],
                    label=destination['label'],
                ) for destination in self.__destinations
            ],
          
            on_change=self.navigation_bar_change
        )
    

    def navigation_bar_change(self, e):
        if self.callback is not None:

            self.callback(self.selected_index)