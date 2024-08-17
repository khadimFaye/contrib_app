from flet import (
    NavigationRail,
    NavigationRailDestination,
    Control,
    colors,
    icons,
    padding,
    border,
    border_radius,
    Badge
)
import flet as ft

from typing import List, Union


class Navrail(NavigationRail):
   
    __destinations = [
        {
            'icon' : icons.HOME_OUTLINED,
            'label' : 'homse', 
            'selected_icon' : icons.HOME_FILLED
        },

        # {
        #     'icon' : icons.HISTORY_OUTLINED,
        #     'label' : 'logs', 
        #     'selected_icon' : icons.HISTORY
        # },

        { 
            'icon' : icons.ADMIN_PANEL_SETTINGS_OUTLINED,
            'label' : 'admin', 
            'selected_icon' : icons.ADMIN_PANEL_SETTINGS
        },
        # { 
        #     'icon' : icons.NOTE_OUTLINED,
        #     'label' : 'note', 
        #     'selected_icon' : icons.NOTE_ROUNDED
        # },
        { 
            'icon' : icons.SETTINGS_OUTLINED,
            'label' : 'impostazioni', 
            'selected_icon' : icons.SETTINGS
        },

        
        ]
    def __init__(self, destinations : List[dict] = None, callback = None):
        self.destinations = destinations or self.__destinations        
        self.callback = callback

        super().__init__(
            indicator_color=colors.PURPLE_300,
            indicator_shape=ft.RoundedRectangleBorder,
            width=0,
            min_width=0,
            min_extended_width=100,
            elevation=10,
            extended=False,
            visible=False,
            animate_size=(ft.Animation(duration=100*4, curve=ft.AnimationCurve.EASE_IN_TO_LINEAR)),
            # on_animation_end=ft.Animation(duration=2, curve=ft.AnimationCurve.FAST_OUT_SLOWIN),
            # height=200,
            bgcolor=colors.PURPLE_600,
            # leading=ft.ElevatedButton(
            #     icon=icons.HOME,
            #     icon_color= 'black'
            # ),
            group_alignment=-0.10,
            selected_index=0,
            on_change=self.change_destination,
            
            destinations=[
                NavigationRailDestination(
                    icon_content = ft.Icon(name = destination['icon'], color='white'),
                    label_content=ft.Text(value=destination['label'], color='white'),
                    selected_icon_content = ft.Icon(name = destination['selected_icon'], color=colors.PURPLE_600),
                    ) for destination in self.destinations
                    ]
        )
    def change_destination(self, e:ft.ControlEvent):
        if self.callback is not None:
           self.callback(self.selected_index)
    # def update_controls(self,*args):
    #     for control in self.destinations:
    #         if self.visible==False:
    #             control.icon_content.visible = False
    #             control.label_content.visible=False
    #             control.selected_icon_content.visible=False
    #         else:
    #             control.icon_content.visible = True
    #             control.label_content.visible=True
    #             control.selected_icon_content.visible=True
            
    #         print('aggiornato')
    #     self.update()
                
    # def opening_animatio(self,e):
        
           

        