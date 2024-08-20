import flet as ft
from flet import *
from ..custums.navigationRail import Navrail
from app.custums.navigationbar import menuBarButton
from .home import Home
from .request_handler import RQ
from app.pages.logs_page import LogsPage
# from ..utils.view import view_handler, change_route


class MainApp(Column):
    __max_extende_value = 120
    
    def __init__(self, page):
        self._page = page
        self.HOME = Home(self._page, menuOpener = self.open_menu)
        self.request_handler = RQ(self._page, callback=self.open_menu , badge=self.HOME.badge)
        self.NAVRAIL = Navrail(callback=self.change_destination)
        self.LogPage = LogsPage(self._page, self.open_menu)
        self._page.overlay.append(self.NAVRAIL)
        self._page.data['control'] = self.HOME.badge
       
        # self._page.navigation_bar = Navbar(callback=self.change_destination) if self._page.platform.value!='windows' else None
        self.content_column = Column(expand=True,controls=[self.HOME])
        # self.nav_row = ft.Row(
        #     vertical_alignment=ft.CrossAxisAlignment.START,
        #     controls =[
        #         ft.Container(
        #             border_radius=4, 
        #             bgcolor=colors.BLUE_500,
        #             expand = False,
        #             content = None)])

        self.MainRow = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            controls= [
                # ft.Container(
                #     height = 600, 
                #     border_radius=12,
                #     bgcolor=ft.colors.BLUE_500,
                #     content=self.nav_row,
                #     visible=True if self._page.platform.value == 'windows' else False
                #     ),
                self.content_column
                ])
        
        super().__init__(
            expand=True,
            controls=[
                self.MainRow
            ]
        )
    def change_destination(self, index):
        print('cambito')
        index_map = {
            '0':self.HOME,
            '2' : self.request_handler,
            '1' : self.LogPage
        }

        if index_map.get(str(index)) is not None:
                
        
            self.content_column.controls=[index_map[str(index)]]
            self.update()
            
            if index==0:
                self.HOME.refresh_logs()
                    
            elif index ==2:
                self.LogPage.flag=True if len(self._page.data['logs'])!=0 else False
                if self.LogPage:
                    self.LogPage.listview.controls = self._page.client_storage.get('logs')
            self.open_menu()
            
    def change_destination_for_other_platform(self, e):
       
        destination = e.control.content.controls[-1].value
        index_map = {
            'Home':self.HOME,
            'admin' : self.request_handler
        }

        if index_map.get(destination) is not None:
          
            self.content_column.controls=[index_map[destination]]
            self.update()
            
    def open_menu(self, *args):
        print(args)
        
        self.NAVRAIL.visible = True if self.NAVRAIL.visible==False else False
        self.NAVRAIL.width = self.__max_extende_value if self.NAVRAIL.width==0 else 0
        # self.NAVRAIL.update_controls()
        self.NAVRAIL.update()
        self.update()
        self._page.update()
        
    def check_platform(self,*args):
        if self._page.platform.value == 'windows':
            return True
        return False
        
# <