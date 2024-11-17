from data_generator import pd
from pathlib import Path
from data_generator import np
import json


def generate_events_documents(events, events_with_location, events_with_person, related_to, event_with_objects):
    event_collection = {}

    for index, row in events.iterrows():

        event = {
            "_id": {
                "$oid": row['id_event']
            },
            "description": row['description'],
            "data": row['event_date'],
            "status": row['status'],
            "luogo": {
                "street_name": events_with_location[events_with_location['id_event'] == row['id_event']][
                    'street_name'].item(),
                "building_number": events_with_location[events_with_location['id_event'] == row['id_event']][
                    'building_number'].item(),
                "city": events_with_location[events_with_location['id_event'] == row['id_event']]['city'].item(),
                "state": events_with_location[events_with_location['id_event'] == row['id_event']]['state'].item(),
                "country": events_with_location[events_with_location['id_event'] == row['id_event']]['country'].item(),
                "postal_code": events_with_location[events_with_location['id_event'] == row['id_event']][
                    'postal_code'].item(),
            },
            "linked_to": [],
            "related_objects": [],
            "related_events": []
        }
        # prende tutte le persone legate all'evento corrente
        all_person_related_to_current_event = events_with_person[events_with_person['id_event'] == row['id_event']][
            'id_person'].tolist()

        # modifica l'id sostituendolo con l'object id
        for index, id in enumerate(all_person_related_to_current_event):
            new = {
                "$oid": id
            }
            all_person_related_to_current_event[index] = new

        if all_person_related_to_current_event:
            event['linked_to'].extend(all_person_related_to_current_event)

        # prende tutti gli eventi legati all'evento corrente
        all_events_related_to_current_event = related_to[related_to['id_event1'] == row['id_event']][
            'id_event2'].tolist()

        for index, id in enumerate(all_events_related_to_current_event):
            new = {
                "$oid": id
            }
            all_events_related_to_current_event[index] = new

        if all_events_related_to_current_event:
            event['related_events'].extend(all_events_related_to_current_event)



        all_objects_related_to_current_event = event_with_objects[event_with_objects['id_event'] == row['id_event']]['id_object'].tolist()

        for index, id in enumerate(all_objects_related_to_current_event):
            new = {
                "$oid": id
            }
            all_objects_related_to_current_event[index] = new

        if all_objects_related_to_current_event:
            event['related_objects'].extend(all_objects_related_to_current_event)

        event_collection[row['id_event']] = event



    for event in event_collection.values():
        curr_event_id = event['_id']['$oid']
        related_event_ids = event['related_events']

        for related_event_id in related_event_ids:
            doc = event_collection[related_event_id['$oid']]
            if curr_event_id not in doc['related_events']:
                doc['related_events'].append({'$oid':curr_event_id})

    with open('events.json', 'w') as f:
        for record in list(event_collection.values()):
            # Converti ogni dizionario in una stringa JSON e scrivilo su una nuova riga
            f.write(json.dumps(record) + "\n")


def generate_objects_documents(object_entities, people, location_entities, events, founded_in, owns, involved_in,
                               dataset_dir):
    # Join tra oggetti e proprietari
    objects_with_owners = object_entities.merge(owns, left_on='id_object', right_on='id_object', how='left')
    objects_with_owners = objects_with_owners.merge(people[['id_person', 'first_name', 'last_name']],
                                                    left_on='id_person', right_on='id_person', how='left')

    # Join tra oggetti e luoghi di ritrovamento
    objects_with_locations = objects_with_owners.merge(founded_in, left_on='id_object', right_on='id_object',
                                                       how='left')
    objects_with_locations = objects_with_locations.merge(
        location_entities[['id_location', 'street_name', 'city', 'state', 'postal_code']],
        left_on='id_location', right_on='id_location', how='left')

    # Join tra oggetti ed eventi associati
    objects_with_events = objects_with_locations.merge(involved_in, left_on='id_object', right_on='id_object',
                                                       how='left')
    objects_with_events = objects_with_events.merge(events[['id_event', 'event_type', 'description', 'event_date']],
                                                    left_on='id_event', right_on='id_event', how='left',
                                                    suffixes=('', '_event'))

    # Pre-processamento: Converti NaN in None e forza i tipi delle colonne numeriche
    objects_with_events = objects_with_events.replace({np.nan: None})

    # Converti tutte le colonne di tipo int64 e float64 nei tipi standard Python int e float
    for col in objects_with_events.select_dtypes(include=['int64', 'float64']).columns:
        objects_with_events[col] = objects_with_events[col].astype(object)

    # Creazione della struttura JSON
    objects_json = []
    grouped_objects = objects_with_events.groupby('id_object')  # Raggruppa per oggetto per unire eventi multipli

    for object_id, group in grouped_objects:
        row = group.iloc[0]  # Prende la prima riga del gruppo per i dettagli unici dell'oggetto

        obj = {
            "_id": row['id_object'],
            "descrizione": row.get("type", "Oggetto senza tipo"),
            "numero_seriale": row.get("serial_number", "Seriale non disponibile"),
            "proprietario": row['id_person'],
            "eventi_associati": [{"$oid" : e} for e in group['id_event'].dropna().unique()],
            "luogo_ritrovamento": {
                "indirizzo": row.get("street_name", "Indirizzo non disponibile"),
                "città": row.get("city", "Città non disponibile"),
                "provincia": row.get("state", "Provincia non disponibile"),
                "Cap": row.get("postal_code", "CAP non disponibile")
            }
        }

        objects_json.append(obj)

    try:
        # Scrittura dell'output JSON con ogni documento su una riga
        with open(dataset_dir.joinpath("objects_data.json"), "w", encoding="utf-8") as f:
            for obj in objects_json:
                json_str = json.dumps(obj, ensure_ascii=False)
                f.write(json_str + "\n")
        print("File JSON generato correttamente con ogni documento su una riga.")
    except Exception as e:
        print(f"Errore durante la scrittura del JSON: {e}")


def generate_person_documents(people, df_residence_in, df_linked_to, collaborate_with):
    people_collection = {}
    not_inserted_yet = {}

    for index, row in people.iterrows():
        curr_person_id = {
            "$oid" : row['id_person']
        }

        persona = {
            "_id": curr_person_id,
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "gender": row["gender"],
            "nationality": row["nationality"],
            "relationship_status": row["relationship_status"],
            "phone_number": row["phone_number"],
            "email": row["email"],
            "date_of_birth": row["date_of_birth"],
            "occupation": row["occupation"],
            "status": row["status"],
            "residence": {},
            "involved_in": [],
            "collaborate_with": []
        }

        if curr_person_id['$oid'] in df_residence_in['id_person'].values:
            curr = df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]

            persona["residence"] = {
                "street_name": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]['street_name'].item(),
                "building_number": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']][
                    'building_number'].item(),
                "city": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]['city'].item(),
                "state": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]['state'].item(),
                "country": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]['country'].item(),
                "postal_code": df_residence_in[df_residence_in['id_person'] == curr_person_id['$oid']]['postal_code'].item(),
            }



        if curr_person_id['$oid'] in df_linked_to['id_person'].values:
            people_involved_in = df_linked_to[df_linked_to['id_person'] == curr_person_id['$oid']]['id_event'].values.tolist()
            for index , person_id in enumerate(people_involved_in):
                new = {
                    "$oid": person_id,
                }
                people_involved_in[index] = new

            persona["involved_in"] = people_involved_in


        if curr_person_id['$oid'] in collaborate_with['id_person1'].values:
            people_collaborate_with = collaborate_with[collaborate_with['id_person1'] == curr_person_id['$oid']]['id_person2'].values.tolist()

            for index , person_id in enumerate(people_collaborate_with):
                new = {
                    "$oid": person_id,
                }
                people_collaborate_with[index] = new
            persona["collaborate_with"] = people_collaborate_with

            not_inserted_yet[curr_person_id['$oid']] = people_collaborate_with

        people_collection[curr_person_id['$oid']] = persona

    for id, list_people in not_inserted_yet.items():
        print(f"{id}: {list_people}")
        for a in list_people:

            people_collection[a['$oid']]['collaborate_with'].append({'$oid':id})

    with open('people_collection.json', 'w') as f:
        for record in list(people_collection.values()):
            # Converti ogni dizionario in una stringa JSON e scrivilo su una nuova riga
            f.write(json.dumps(record) + "\n")


def main():
    # entities
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")
    relationships_dir = base_dir.joinpath("dataset", "relationships")

    people = pd.read_csv(dataset_dir.joinpath("people_data.csv"))
    people.rename(columns={'id': 'id_person'}, inplace=True)

    events = pd.read_csv(dataset_dir.joinpath("events_data.csv"))
    events.rename(columns={'id': 'id_event'}, inplace=True)

    location_entities = pd.read_csv(dataset_dir.joinpath("location_data.csv"))
    location_entities.rename(columns={'id': 'id_location'}, inplace=True)

    object_entities = pd.read_csv(dataset_dir.joinpath("objects_data.csv"))
    object_entities.rename(columns={'id': 'id_object'}, inplace=True)

    # relationships object_entity_id
    residence_in = pd.read_csv(relationships_dir.joinpath("residence_in.csv"))
    linked_to = pd.read_csv(relationships_dir.joinpath("linked_to.csv"))
    collaborate_with = pd.read_csv(relationships_dir.joinpath("collaborate_with.csv"))
    founded_in = pd.read_csv(relationships_dir.joinpath("founded_in.csv"))
    owns = pd.read_csv(relationships_dir.joinpath("owns.csv"))

    involved_in = pd.read_csv(relationships_dir.joinpath("involved_in.csv"))

    happened_in = pd.read_csv(relationships_dir.joinpath("happened_in.csv"))

    related_to = pd.read_csv(relationships_dir.joinpath("related_to.csv"))

    df_partial_join_linked_to = pd.merge(linked_to, people, on='id_person', how='left')
    df_linked_to = pd.merge(df_partial_join_linked_to, events, on='id_event', how='left')

    df_partial_join_residence_in = pd.merge(residence_in, people, on='id_person', how='left')
    df_residence_in = pd.merge(df_partial_join_residence_in, location_entities, on='id_location', how='left')

    events_with_location_partial_join = pd.merge(happened_in, events, on='id_event', how='left')
    events_with_location = pd.merge(events_with_location_partial_join, location_entities, on='id_location', how='left')

    events_with_person_partial_join = pd.merge(linked_to, events, on='id_event', how='left')
    events_with_person = pd.merge(events_with_person_partial_join, people, on='id_person', how='left')

    events_with_objects_partial_join = pd.merge(involved_in, events, on='id_event', how='left')
    event_with_object_join = pd.merge(events_with_objects_partial_join, object_entities, on='id_object', how='left')

    generate_person_documents(people, df_residence_in, df_linked_to, collaborate_with)
    generate_objects_documents(object_entities, people, location_entities, events, founded_in, owns, involved_in,
                               dataset_dir)
    generate_events_documents(events, events_with_location, events_with_person, related_to, event_with_object_join)


if __name__ == '__main__':
    main()
