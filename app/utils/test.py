from functions import get_schede

argomento = "Definizioni generali e doveri nell'uso della strada"

for i in range(1,len(get_schede(argomento))+1):
    scheda = get_schede(argomento)
    prima_domanda = scheda.get(str(i))[0]['domanda']
    print(f' ** [ {i} : {prima_domanda}] **',end='\n\n')