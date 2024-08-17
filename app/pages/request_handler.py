from flet import *
from ..custums.request_card import RequestCard
# from ..utils.encription import IO, encrypt, decrypt, Key
from ..utils.secure_storage import *
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from ..custums.snackbar import CustomSnackbar

# dotenv_path = os.path.join(os.getcwd(),'FRONTEND','resources','.env')
# load_dotenv(dotenv_path)

URL_base = 'https://samaserver-51970f571916.herokuapp.com'
# URL_base = 'http://127.0.0.1:3000'
ENDPOINT = "fetch_requests"

class RQ(Container):
    # __key__ = Key().load_key() or Key().generate_fernet_key(autosave=True)
    def __init__(self, page):
        self._page = page
        self.counter = Text(value = None, color=colors.BLACK54, size = 14, weight='w700')
        self.listview = ListView(spacing=8)
        self.list_users = GridView(runs_count=1,spacing=8,)

        super().__init__(
            bgcolor=colors.with_opacity(0.95, 'white'),
            padding = 15,
            border_radius=12,
            # height=500,
            content=Column(
                # scroll=ScrollMode.HIDDEN,
                 controls=[
                    Container(
                       expand = False,
                        padding = 10,
                        bgcolor = 'white',
                        content=Row(
                                controls=[
                                Row(
                                    alignment=MainAxisAlignment.START, 
                                        controls = [
                                            
                                            Icon(
                                                name = icons.ADMIN_PANEL_SETTINGS,
                                                color=colors.BLUE_700,
                                            ),
                                            Text(
                                                value = 'area admin'.title(), 
                                                weight='w600', 
                                                size = 20,
                                                color=colors.BLACK87),
                                            
                                            ]),
                                    
                                ]
                        )
                    ),
            #counter
            Container(),
            Row(controls = [Container(),]),
            #divider


            #listview
            Tabs(

                label_color='black',
                unselected_label_color=colors.BLACK54,
                indicator_color=colors.PURPLE_600,
                # height = 400,
                expand = 1,
                tabs=[
                    Tab(
                        adaptive=True,
                        text='Richieste', 
                        content= Container(
                            content = Column(
                                scroll = ScrollMode.HIDDEN,
                            controls=[
                                Container(),
                                Row(
                                    alignment=MainAxisAlignment.END,
                                    expand = False,
                                    controls = [
                                        IconButton(
                                            icon=icons.REFRESH,
                                            on_click=self.load_request
                                        )
                                        ]
                                    ),
                                # self.counter,
                                    self.listview])),
                        icon=icons.INBOX_ROUNDED),

                    Tab(text="user management",
                content=Container(
                    content=Text("This is Tab 1")
                )),]
            ),
           
                ]
            ),
        expand=True,
        )
        
    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.add(snackbar)
        self._page.open(snackbar)

    
    def clear(self,*args):
        self.listview.controls=[]
        self.update()
    
    def check_if_childs_exists(self, *args):
        if self.listview.controls!=[]:
            self.clear()
        else:
            print('children')
          
       

    def load_request(self, *args):
        
        self.clear()
        try:
            
            data = self.send_translate_request()
            self.counter.value = str(len(data)) if data is not None else str('0')
        
        
       
            if data is not None and data !=[]:
                
                for i in data:
                    print(i['id'])
                    self.listview.controls.append(
                        RequestCard(
                            refresh=self.load_request,
                            page=self._page, 
                            username=i["username"],
                            index=i["index"], 
                            questionIndex=i["id"], 
                            traduction_text=i["valore"], 
                            argomento=i['arg'],
                            question=i["question"],
                            request_id =i['request_id'] ,
                            timestamp=f"{datetime.fromtimestamp(i['timestamp'])}"))

                    self.update()
                    
            else:
                if os.getenv('admin')!='True':
                    self.listview.controls.append(self.excpetion_illustration(message = 'Accedi con un account che dispone dell\'autorizzazione!', image = Image(src='/No_Auth.gif')))
                    self.update()
                else:
                
                    self.listview.controls.append(self.excpetion_illustration())
                    self.update()
       
        finally:
            self.update()

        

    def send_translate_request(self,*args):
        url = f'{URL_base}/{ENDPOINT}'
       # params = {"argomento":self.argomento,"value" :self.traduction_label.value,"n": self.n, "index": self.index}
        token = get_token("mytoken", os.getenv('sub'))
        headers = {'Authorization' : f'Bearer {token}'}
        response = requests.get(url=url, headers=headers)
        if response.status_code==200:
            return response.json()
        
        elif response.status_code==401:
            self.set_snackbar(message='l\'utente non é autorizzato per accedere in questa area!', color='red')
        return None
    
    def excpetion_illustration(self,message:str ='Nessuna richiesta!', image: Control = Icon(name=icons.INBOX_ROUNDED, size=30, color='grey')):
        
        return Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=False,
            controls=[
                image,
                Text(value=message, color = colors.BLACK87)]
            )
                