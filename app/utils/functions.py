import flet as ft
import time
import json
import threading
import os
import pprint
print(os.path.join(os.getcwd()))
def get_args(*args):
        dir_name =  'app/resources'
        filename = 'argomenti.json'
        path = os.path.join(os.getcwd(),dir_name, filename)
        with open (path,'r') as f:
            data = json.load(f)
            argomenti = [n.get('arg') for n in data]
       
       
        return argomenti

def get_schede(key : str):
    
    dir_name =  'app/resources'
    filename = 'schede.json'
    path = os.path.join(os.getcwd(),dir_name, filename)
    
    with open (path,'r') as f:
        data = json.load(f)
        try:
            scheda = data.get(key)['schede'] if data.get(key) is not None else None
            #print(scheda)
            return scheda
        except KeyError as e :
            return None
        
def read_json_file(*args):
    
    dir_name =  'app/resources' 
    filename = 'schede.json'
    path = os.path.join(os.getcwd(),dir_name, filename)
   
    with open (path,'r') as file:
        try:
            data = json.load(file)
            return data
        except KeyError as e :
            return None
        
    
    

# def domanda_successiva(self, event):
#     # index = instance.index
#     # ID = instance.id
#     expansiontile_instance = event.control.data[0]
#     text_area__instance = event.control.data[1]

#     key = event.control.data[2]
#     index = expansiontile_instance.index
#     Id = expansiontile_instance.ID
#     index_label = event.control.data[3]

#     scheda = get_schede(key)
#     # print(key, index)
#     if event.control.data[0].index<30 and event.control.icon =='chevron_right':
#         expansiontile_instance.index+=1
#         expansiontile_instance.counter+=1
        
        
#         text_area__instance.content.value = scheda[str(event.control.data[0].ID)][event.control.data[0].index]['domanda']
#         index_label.controls[1].value = f'domanda:{event.control.data[0].counter}'

#     else:
#         if index>0 or index>=1:
#             print('left')
#             expansiontile_instance.index-=1
#             expansiontile_instance.counter-=1
            
            
#             text_area__instance.content.value = scheda[str(expansiontile_instance.ID)][expansiontile_instance.index]['domanda']
#             index_label.controls[1].value = f'domanda:{expansiontile_instance.counter}'
#     self.update()

# def scheda_successiva(self, instance, data, event):

#     try:
#         instance.ID+=1
#         event.value = data[instance.ID][instance.index]['domnda']
#     except KeyError as e :
#         print('fuori range') 
#     finally:
#             self.update()


def traduci(self, event):
    event.control.visible = False
    print(event.control)
    event.control.data.get('traductionsumbit').visible = True
    event.control.data.get('traduzioneinput').visible = True
    event.control.data.get('traduzioneinput').value = ''
    # event.control.data[0].controls[0].visible = True
    # print(event.control.data.control)
    self.update()
     
def confirma(self, event):
    # event.control.visible =False
    # event.control.data.get('translatbutton').controls[0].visible = True
    TraduzioneInput = event.control.data.get('traduzioneinput')
    key = event.control.data.get('key').content.value
    # TraduzioneInput.visible = False

    # # print(event.control.data)
    # self.dialog.data = event.control.data
    self.dialog.data = {'sumbitbutton' : event.control, 'translatbutton': event.control.data.get('translatbutton'), 'key' : key, "traduzioneinput": TraduzioneInput, "expansiontile":event.control.data.get("expansiontile")}
    self.dialog.open = True
    
    self.update()

def close_dialog(self, *args):
    print(self)
    Expansiontile = self.dialog.data.get("expansiontile")
    #key 
    key = self.dialog.data.get('key')
   
    #id
    Id = str(Expansiontile.ID)
    #index
    index = Expansiontile.index
    input_traduction = self.dialog.data.get("traduzioneinput")
    value=input_traduction.value #value
    if args[0].control.text == 'si'.capitalize()and value != '' :
        input_traduction.visible = False
        self.dialog.open = False

        self.dialog.data.get('translatbutton').visible = True
        self.dialog.data.get('sumbitbutton').visible = False
        tdt = self.dialog.data.get('sumbitbutton').data.get('tdt')
        update_data(self, key, index, Id, value, tdt=tdt)
    else:
        self.dialog.open =False
        self.dialog.data.get('translatbutton').visible = True
        self.dialog.data.get('sumbitbutton').visible = False
        self.snack_bar.content.value = 'Non lasciare il campo vuoto'
        input_traduction.visible = False
        self.snack_bar.open=True
    
    self.update()

def update_data(self, key, index, Id, value, tdt):
    """aggiorna i il json file """
    data = read_json_file()
    print(key, index)
    if data is not None:
        try:
            if data.get(key) is not None :
                data.get(key)['schede'][Id][index]['wolof'] = value
                tdt.Value+=1
                
                print(tdt.Value)
                
                data['TDT'] = int(tdt.Value)
                # pprint.pprint(data.get(key)['schede'][Id][index])
                save_change(data)

                self.snack_bar.content.value = 'Traduzione aggiornata con successo'
                self.snack_bar.open = True
                # self.update()
        except KeyError as e :
            print(str(e))
        finally:
            self.update()

def save_change(data):
    dir_name =  'app/resources' if os.getcwd().split('\\')[-1] == 'contrib_platform' else 'resources'
    filename = 'schede.json'
    path = os.path.join(os.getcwd(),dir_name, filename)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=5)
    

def preview(self, button_instance):
    if button_instance.control.text =='kholal':

        #nascondi il bottone cliccato
        button_instance.control.visible = False
        instances = button_instance.control.data
        

        #bottone per nascondere il text area
        hide_button = instances.get('hide_button')
        hide_button.visible = True#nascondi

        key : str = instances.get('key') #argomento seklezioanto
        ID : str = str(instances.get('id')) # id della scheda da selezioanre
        index: int = instances.get('index') # index delle domande

    

        #read json file e controlla se la domanda  attuale é stata tradotta  o no 
        data = read_json_file()
        if data is not None:
            traduzione = data[key]['schede'][ID][index]['wolof']
            if traduzione !='jappandi wul':
                instances.get('traduzione_input').value = traduzione
            else:
                instances.get('traduzione_input').value = ' non ancora tradotto'
        else :
            print('argomnento non trovato')
        instances.get('traduzione_input').visible=True
        instances.get('traduzione_input').read_only = True
        instances.get('traduzione_input').bgcolor = ft.colors.GREY_600
    elif button_instance.control.text == 'neubal':

        button_instance.control.visible = False
        instances = button_instance.control.data

        instances.get('preview_button').visible =True

        instances.get('traduzione_input').visible=False
        instances.get('traduzione_input').read_only = False
        instances.get('traduzione_input').value = ''
        


    self.update()


def readJsonFile(file_name : str ,dir:str = None, mode :str = 'r') -> dict:
    dir = 'app/config/systeme_configuration_file.json' if  os.getcwd().split('//')[-1]=='contrib_platform' else 'config/systeme_configuration_file.json'
    path = os.path.join(os.getcwd(),dir)  #if dir not in os.getcwd() else os.path.join(os.getcwd(),file_name)
    try:
        with open(path,mode='r', encoding='utf-8') as f:
            data = json.load(f)
            return  data
        #[i.get('arg') for i in data]

    except FileNotFoundError as e:
        print(str(e))
    



        

        
def check_system_linguage(*args) -> str:
    try:
        system_data = readJsonFile('../app/config/systeme_configuration_file.json')
        print(system_data)
        # return system_data.get('$linguage')
    except KeyError as e:
        print(str(e))
    except FileNotFoundError as e:
        print(str(e))

    




def set_transtion(page, platform ,mode = 'none'):
    try :

        mods = {
            'none' : ft.PageTransitionTheme.NONE,
            'zoom' : ft.PageTransitionTheme.ZOOM,
            'cupertino' : ft.PageTransitionTheme.CUPERTINO
        }
        theme  = ft.Theme()
        page.theme = theme
        if platform =='ios':
            theme.page_transitions.ios = mods[mode]
        else:
            theme.page_transitions.windows = mods[mode]
    except KeyError as e:
        print(f'{mode} non valido scegli tra quiesti [none, zoom, cupertino]')

def check_platorm(page):
   return page.platform.value
   
def change_view(page, e,route:str=None):
        route = e.control.data if route is None else route
        set_transtion(page,platform=check_platorm(page),mode='zoom')
        page.go(route)



def get_ttd():
    N = []
    args = get_args()
    try:

        if args is not None:
            for arg in args:
                scheda = read_json_file().get(arg)
                if scheda !=None:
                    scheda.get('schede')
                    s = (len(list(scheda.values())[0].values()))
                    if s !=[] or s is not None:
                        # print('..............................................................................................................',end='\n\n')
                        tt = 30 *s
                        N.append(tt)
        return sum(N) if sum !=[] else None
    except Exception as e:
        print(str(e))

def get_tsd():
    N = []
    args = get_args()
    try:

        if args is not None:
            for arg in args:
                scheda = read_json_file().get(arg)
                if scheda !=None:
                    s = scheda.get('schede').keys()
                    if s !=[] or s is not None:
                        suM = (len(scheda.get('schede').keys()))
                        # print('..............................................................................................................',end='\n\n')
                        
                        N.append(suM)
        return sum(N) if sum !=[] else None
    except Exception as e:
        print(str(e))

def get_tdt():
    N = 0
    args = get_args()
    scheda  = get_schede()
    try:

       
        return N if N else 0
    except Exception as e:
        print(str(e))
    finally:
        print(N)
        return N

def select(self, event, argoment_area, bottomsheetInstance, deletinstance, listview):
    argoment_area.content.bgcolor = ft.colors.GREY_600
    argoment_area.content.value = event.control.text
    setattr(bottomsheetInstance, 'open', False)
    if listview.controls!=[]:
        deletinstance.icon_color = 'red'
        deletinstance.disabled = False
   
    # if idselector.value =='':
    #     idselector.error_text= 'tannal id scheda bi'
   

    self.update()

def unselect(self, event, argoment_area, listview):
    event.control.disabled = True
    argoment_area.content.value = ''
    argoment_area.content.bgcolor = ''
    event.control.icon_color = ''
    # argoment_area.bgcolor = ''
    listview.controls = []

    self.update()



        

     
