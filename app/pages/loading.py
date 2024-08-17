from flet import *
import time
import threading

from ..utils.secure_storage import *
from jose import ExpiredSignatureError, JWTError
# from fastapi import HTTPException, status
from ..custums.snackbar import CustomSnackbar
from dotenv import set_key, load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

class Loading(Container):
    __flag : bool = False
    def __init__(self, page):
        self._page = page
        super().__init__(
            # padding=10,
            # margin=margin.all(10.0),
            border_radius=12,
            width = 320, 
            height=300,
            animate_scale=Animation(200*2, curve=AnimationCurve.EASE),
            bgcolor = 'white',
            content=Column(
                
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls = [

                    Row(
                        alignment = MainAxisAlignment.CENTER,
                        controls=[ProgressRing(
                        stroke_align=StrokeCap.BUTT,
                        stroke_width=8,
                        bgcolor=colors.PURPLE_600,
                        width = 100,
                        height = 100,
                        color='white'

                    )]),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[Text(value='Autenticazione in corso....', color = colors.BLACK87, size = 13)]
                    )
                ]
            )
        )
        
        # threading.Thread(target=self.start_animation).start()
        # threading.Thread(target=self.on_enter).start()

    def start_animation(self, *args):
        self.scaleUp()
        time.sleep(0.5)
        self.scaleDown()
        
        if not self.__flag:
            return self.start_animation()

    def scaleUp(self,*args):
        self.scale = 1.5
        time.sleep(0.5)
        # self.update()

    
    def scaleDown(self,*args):
        self.scale = 1
        time.sleep(0.5)
        # self.update()
    
    def set_snackbar(self, message, color):
        snackbar = CustomSnackbar(message=message, bgcolor=colors.with_opacity(0.70, f'{color}'))
        self._page.show_snack_bar(snackbar)
    
    def on_enter(self,*args):
        time.sleep(1.2)
        try:

            username = os.getenv('sub')
            token = get_token(service_name='mytoken', username=username)
           
            payload = jwt.decode(token = token, key=os.getenv('secret_key'), algorithms=[os.getenv('ALGORITHM')])

            activce_user = payload.get('sub')
            if activce_user is None:
                self.set_snackbar(message='fai il login di nuovo:(', color='red')
                print(str(e))
            else:
                self.set_snackbar(message='utente autentificato!', color='green')
                self._page.go('/')
              


                # response = requests.post(url=url,)
        except ExpiredSignatureError as e:
            print(str(e))
            self.set_snackbar(message='sessione terminata fai il login di nuovo:(', color='red')
            self._page.go('login')
            # raise ValueError('sessione terminata fai il login di nuovo')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )
        except JWTError:
            self.set_snackbar(message='sessione terminata fai il login di nuovo:(', color='red')
            self._page.go('login')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='fai il login di nuovo'
            #     )
                
        except AttributeError:
            self.set_snackbar(message='sessione terminata fai il login di nuovo:(', color='red')
            self._page.go('login')
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail='sessione terminata fai il login di nuovo'
            # )
            # raise AttributeError(name='sessione terminata fai il login di nuovo')
        
        
            
       
        

    # def start(self, *args):
    #     if os.getenv('sub') is not None :
    #         threading.Thread(target=self.start_animation).start()
    #         threading.Thread(target=self.on_enter).start()
    #     else:
    #         self.go('login')

    


