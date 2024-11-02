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

