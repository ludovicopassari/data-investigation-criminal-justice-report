from data_generator.generator_config import person_attributes, object_attributes, event_attributes, location_attributes, \
    evidence_attributes
from data_generator import generate_data
from pathlib import Path

# Ottenere il percorso del file Python in esecuzione
current_file_path = Path(__file__).resolve()

# Ottenere la directory corrente
output_path = current_file_path.parent.parent.parent.joinpath('dataset')

people_path = output_path.joinpath('people_data.csv')
events_path = output_path.joinpath('events_data.csv')
objects_path = output_path.joinpath('objects_data.csv')
location_path = output_path.joinpath('location_data.csv')
evidence_path = output_path.joinpath('evidence_data.csv')

people = generate_data(45, person_attributes, 'csv', people_path)
events = generate_data(30, event_attributes, 'csv', events_path)
objects = generate_data(15, object_attributes, 'csv', objects_path)
location = generate_data(15, location_attributes, 'csv', location_path)
evidence = generate_data(15, evidence_attributes, 'csv', evidence_path)


"""
--- IMPORTAZIONI DEI MODULI --- 
Questo script genera un set di dati sintetici utilizzando il modulo data_generator con l'obiettivo di creare e salvare diversi file CSV che contengno dati fittizi
relativi a persone, eventi, oggetti, luoghi e prove.
I vari attributi (come person_attributes) predefiniti sono utilizzati per generare dati relativi alle varie entità e
vengono importati dal modulo generator_config all'interno di data_generator

generate_data : E' la funzione che genera i dati in base agli attributi specificati e li salva in un formato richiesto (nel nostro caso CSV)
path : E' una classe del modulo pathlib che gestisce i percorsi dei file in modo robusto rispetto all'uso delle semplici stringhe.

--- PERCORSI DEI FILE ---
current_file_path = Path(__file__).resolve() Questa riga ottiene il percorso completo del file python attualmente in esecuzione( lo script stesso) usando __file__,
invece con resolve() risolve il percorso assoluto.
output_path = Definisce la directory di output, che si trova tre livelli sopra la directory corrente e si unisce alla directory 'dataset' utilizzando joinpath('dataset')

--- DEFINIZIONE DEI PERCORSI PER I FILE CSV ---
Qui vengono definiti i percorsi completi dove verrano salvati i file CSV generati, unendo la directory di output_path ai nome dei file. In altre parole andiamo asalvare 
i vari file csv riferiti alle varie entità nella cartella creata precedentemente

--- GENERAZIONE DEI DATI ---
Per ciascuna tipologia di dati, viene chiamat ala funzione generate_data, che genera un numero specifico di record e li salva nei file CSV ai percorsi definiti in precedenza
Ogni chiamata ha quattro parametri : 1) il numero di record da generare 2) gli attributi specifici, questi definiscono la struttura dei dati generati 3) il formato dell'output 
4) il percorso del file
""" 