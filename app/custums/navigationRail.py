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
    def __init__(self, destinations : List[dict] = None, callback = None):
        self.destinations = destinations
        self.callback = callback

        super().__init__(
            indicator_color=colors.BLACK,
            indicator_shape=ft.RoundedRectangleBorder,
            min_width=50,
            min_extended_width=100,
            elevation=10,
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
                    icon = destination['icon'],
                    label=destination['label'],
                    selected_icon= destination['selected_icon'],
                    ) for destination in destinations
                    ]
        )
    def change_destination(self, e:ft.ControlEvent):
        if self.callback is not None:
           self.callback(self.selected_index)
           

        