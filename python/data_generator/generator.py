from data_generator import pd
from bson import ObjectId
import hashlib
import time


def integer_to_objectid(integer):
    hash_value = hashlib.md5(str(integer).encode()).hexdigest()
    timestamp = hex(int(time.time()))[2:].zfill(8)  # Garantisce 8 caratteri
    unique_id = hash_value[:10]  # Prende 10 caratteri
    counter = "001234"  # Deve essere lungo 6 caratteri
    objectid_string = timestamp + unique_id + counter
    return objectid_string  # Restituisce sempre una stringa


def generate_data(entry_num, attribute_list, export=None, path=None):
    data = []
    int_id = 0
    for _ in range(entry_num):
        entry = {attr: funzione() for attr, funzione in attribute_list}
        data.append(entry)
        hex_id = integer_to_objectid(int_id)
        entry['id'] = hex_id
        int_id += 1

    # Creiamo il DataFrame a partire dai dati generati
    df = pd.DataFrame(data)

    if export is None:
        return df
    elif export == 'csv':
        try:
            df.to_csv(path, index=True, index_label='incremental_id')
        except Exception as e:
            print(e)
