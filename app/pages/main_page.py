import flet as ft
from flet import *
from ..custums.navigationRail import Navrail
# from custums.navigationbar import Navbar
from .home import Home
from .request_handler import RQ
# from ..utils.view import view_handler, change_route


class MainApp(Column):
    __max_extende_value = 120
    
    def __init__(self, page):
        self._page = page
        self.HOME = Home(self._page, menuOpener = self.open_menu)
        self.request_handler = RQ(self._page)
        self.NAVRAIL = Navrail(callback=self.change_destination)
       
        # self._page.navigation_bar = Navbar(callback=self.change_destination) if self._page.platform.value!='windows' else None
        self.content_column = Column(expand=True,controls=[self.HOME])
        self.nav_row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls =[
                ft.Container(
                    border_radius=4, 
                    bgcolor=colors.BLUE_500,
                    expand = False,
                    content = self.NAVRAIL)])

        self.MainRow = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            controls= [
                ft.Container(
                    height = 600, 
                    border_radius=12,
                    bgcolor=ft.colors.BLUE_500,
                    content=self.nav_row,
                    visible=True if self._page.platform.value == 'windows' else False
                    ),
                self.content_column
                ])
        
        super().__init__(
            expand=True,
            controls=[
                self.MainRow
            ]
        )
    def change_destination(self, index):
        index_map = {
            '0':self.HOME,
            '1':Text(value='hello'),
            '2' : self.request_handler
        }

        if index_map.get(str(index)) is not None:
          
            self.content_column.controls=[index_map[str(index)]]
            self.update()
    def open_menu(self, e):
        self.NAVRAIL.width = self.__max_extende_value if self.NAVRAIL.width==0 else 0
        # self.NAVRAIL.update()
        self.update()
        
# <