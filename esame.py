#Nome: Spela Ferfoglia
#Matricola: EC2100738
#Corso di laurea: Statistica e informatica per l'azienda, la finanza e l'assicurazione

#-------------------------------------------------------------------------------------

#  Codice programma

#-------------------------------------------------------------------------------------

#classe per alzare le eccezzioni
class ExamException(Exception):
    pass

#classe principale
class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name #iniziallizzo

    def get_data(self):
        
        #INIZIALIZZO una lista dove andro a salvare più liste date da due valori
        lista = []

        #controllo se è stato inserito qualche file
        if self.name is None:
            raise ExamException('Errore, file non inserito')
        
        try: #provo ad aprire il file
            my_file = open(self.name, 'r')
        except Exception as e: #se non riesco ad aprire alzo un eccezzione
            print('Errore nella lettura del file: "{}"'.format(e))
            return None #se alzo l'eccezzione ritorno "nulla/vuoto"
        
        #controllo riga per riga del file
        for line in my_file:
            
            #divido il file in posto ognidove ci sia una virgola
            posto = line.split(',')

            #controllo se ci sono due colonne, se per sbaglio ci sono più o meno collone salto questa riga
            if len(posto) != 2:
                
                continue

            #salto la prima riga che definisce l'ordinamento dei dati (epoch,temperature)
            if posto[0] != 'epoch':

                #assegno a epoch il posto 0 del file
                #assegno a temperature il posto 1 del file    
                epoch  = posto[0]
                temperature = posto[1]
                
                #CONVERSIONE TIPI
                try:
                    epoch = int(epoch) #converto epoch in tipo int
                    temperature = float(temperature) #converto temperature in tipo float

                except: # se non converto vado avanti con il programma
                    
                    continue

                #CONTROLLO DUPLICATI O ORDINAMENTO
                #dichiarazione variabili di sostegno
                prima = 0 
                
                #ciclo che controlla dal primo elemento della lista fino all' ultimo (lunghezza della lista)
                for i in range(len(lista)):
                    #se se il primo è maggiore o uguale a quello dopo alzo un eccezione
                    if prima >= lista[i][0]:
                        raise ExamException ('Errore, duplicato o ordinamento sbagliato')
                    #aggiorno le variabili di sostegno
                    prima = lista[i][0] 
                    i=i+1
               
                #la lista è una lista di liste quindi ne creo un pezzo
                pezzo = [epoch,temperature]
                lista.append(pezzo) #aggiungo il pezzo alla lista principale
        
        my_file.close() #chiudo il file

        #se la lista è vuota alzo un'eccezione
        if not lista: 
            raise ExamException('Errore, file vuoto')
        
        return lista #ritorno la lista che è una lista di liste

def daily_stats(time_series):

    #liste di supporto
    ore = []
    epoche = []

    #creo una lista dove salvo tutte le epoche
    for i in range(len(time_series)):
        epoca = time_series[i][0]
        epoche.append(epoca)

    #creo una lista dove salvo tutte le temperature ora per ora
    for i in range(len(time_series)):
        ora = time_series[i][1]
        ore.append(ora)

    #dichiaro due liste, una conterrà l'altra con dentro le temperature divise giorno per giorno
    giorno = []
    giorni_divisi = []

    j=1
    i=0
    
    #creo una lista che ne contiene un'altra con le temperature divise in giorni
    while i<len(epoche):
        
        #creo il limite della giornata
        limite = (epoche[0] - (epoche[0]%86400)+86400*j)
        
        #aggiungo le temperature alla lista dello stesso giorno, fino a quando non trovo una data >= del limite
        while i < len(epoche) and epoche[i] < limite: 
            agg = ore[i]
            giorno.append(agg)
            i += 1
        
        #aggiorno j solo quando finisco di inserire tutte le temperature dello stesso giorno in una sola lista
        j += 1 
        giorni_divisi.append(giorno) #aggiungo il giorno alla lista che contiene n_liste di giorni
        giorno = [] #azzero la lista del giorno per passare al giorno successivo
        
    #creo una lista dove salverò le statistiche giorno per giorno
    statistiche = []

    #per ogni giorno (nella lista di tutti i giorni) calcolo il minimo, il massimo e la media
    for giorno in giorni_divisi:
        minimo = min(giorno)
        massimo = max(giorno)
        media = sum(giorno) / len(giorno)
        #creo una lista che conterrà il minimo il massimo e la media per ogni giorno
        stat = [minimo,massimo,media]
        #la aggiungo alla lista generale che contiene tutte le statistiche
        statistiche.append(stat)

    #ritorno la lista delle statistiche
    return statistiche

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()


print('\nNome del file: "{}"'.format(time_series_file.name))
print('\nFile: \n"{}"'.format(time_series_file.get_data()))
print('\nStatistiche:')
for line in daily_stats(time_series):
    print(line)