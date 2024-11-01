from data_generator import pd


def generate_data(entry_num, attribute_list, export=None, path=None):
    data = []

    for _ in range(entry_num):
        entry = {attr: funzione() for attr, funzione in attribute_list}
        data.append(entry)

    # Creiamo il DataFrame a partire dai dati generati
    df = pd.DataFrame(data)

    if export is None:
        return df
    elif export == 'csv':
        try:
            df.to_csv(path, index=True, index_label='id')
        except Exception as e:
            print(e)


"""
Tramite questo script  andiamo a generare un insieme di dati sintetici in base a una lista di attributi, e opzionalmente esporta i dati in un file CSV
--- IMPORTAZIONE DI PANDAS ---
Con pd ci riferiamo a pandas, un popolare pacchetto Python per la manipolazione e l'analisi dei dati. Viene importato dal modulo data_generator

--- DEFINIZIONE ELLA FUNZIONE GENERATE_DATA ---
La funzione generate_data si compone dei seguenti parametri : 1) Il numero di record che si vuole generare, 2)La lista di attributi, 
dove ogni attributo è rappresentato da una coppia(attr,funzione) dove attr è il nome dell'attributo e funzioe è una funzione che genera un valore per quell'attributo,
3) export è un parametro opzionale, se specificato ad esempio come CSV, i dati verrano esportati in un file CSV, 4) path è il percorso del file dove verrano salvati i
dati nel caso in cui ad esempio export sia settato su 'csv'

--- GENERAZIONE DEI DATI ---
Per generare i dati viene inizializzata una lista vuota per raccogliere i dati generati.
for _ in range(entry_num): Viene eseguito un ciclo che genera il numero di record specificati da entry_num
entry = {attr: funzione() for attr, funzione in attribute_list} in ogni iterazione viene creato un dizinario dove le chiavi sono i nomi degli attributi e i valori sono 
generati chiamando le rispettive funzioni.
data.append(entry) ogni "entry" (record generato) viene aggiunto alla lista data

--- CREAZIONE DEL DATAFRAME ---
Una volta raccolti i dati, viene creato un DataFrame utilizzando pandas. Un DataFrame è una struttra dati tabellare, simile a una tabella in un database o un foglio di calcolo
ed è l'ideale per manipolare e analizzare dati strutturati.

--- ESPORTAZIONE O RITORNO DEI DATI ---
Questa parte controlla se i dati devono essere esportati o semplicemente restituti.
Se export è none la funzione ritorna il dataframe direttamente senza essere salvati su disco.
Se export è 'CSV' tenta di esportare i dati in un file CSV. Viene utilizzato il metodo to_csv() di pandas
che salva il dataframe nel percorso specificato da path. Index=True indica l'indice delle righe del dataframe ( un numero progressivo) verrà incluso nel CSV. index_label='id' 
specifica che la colonna indice nel CSV sarà etichettata come 'id'

--- GESTIONE DELLE ECCEZIONE ---
Se si verifica un errore durante l'esportazione (ad esempio, se il percorso non esiste o non è accessibile), viene catturata l'eccezione e viene stampato il messaggio di errore
"""