from pathlib import Path
from data_generator import random
from data_generator import pd, np
from tqdm import tqdm


def person_to_event_relationship(people_entities: pd.DataFrame,
                                 event_entities: pd.DataFrame,
                                 max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in tqdm(people_entities.iterrows(), total=people_entities.shape[0],
                           desc="Creating linked_to relationship",
                           unit="row"):
        num_relationships = np.random.randint(0, max_relationship + 1)
        related_b = np.random.choice(event_entities['id'], num_relationships,
                                     replace=False)

        for b_id in related_b:
            relationships.append({'id_person': row['id'], 'id_event': b_id})

    return pd.DataFrame(relationships)


def person_to_person_relationship(people_entities: pd.DataFrame, max_relationship=3):
    relationships = []

    for index, row in tqdm(people_entities.iterrows(), total=people_entities.shape[0],
                           desc="Creating collaborate_with relationship",
                           unit="row"):
        # specifica quante persone devono essere messe in relazione con la persona corrente
        num_relationships = np.random.randint(0, max_relationship + 1)
        # estrae in maniera random un numero di 'id' di persone pari a 'num_relationship' dal dataframe delle le persone
        related_b = np.random.choice(people_entities['id'], num_relationships, replace=False)
        # per ogni persona estratta verifica che essa non sia messa in relazione con se stessa
        for b_id in related_b:
            if b_id != row['id']:
                relationships.append(
                    {'id_person1': row['id'], 'id_person2': b_id})

    return pd.DataFrame(relationships)


def person_to_location(people_entities: pd.DataFrame, location_entities: pd.DataFrame):
    residence_in = []
    for index, row in people_entities.iterrows():
        location_id = []
        has_home = np.random.choice([0, 1], p=[0.8, 0.2])
        if has_home:
            location_id = np.random.choice(location_entities['id'], has_home)
        for id in location_id:
            residence_in.append({'id_person': row['id'], 'id_location': id})
    df = pd.DataFrame(residence_in)
    return df


def event_to_event_relationship(events_entities: pd.DataFrame, max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in tqdm(events_entities.iterrows(), total=events_entities.shape[0],
                           desc="Creating related_to relationship",
                           unit="row"):
        num_relationships = np.random.randint(0, max_relationship + 1)
        related_b = np.random.choice(events_entities['id'], num_relationships,
                                     replace=False)

        for b_id in related_b:
            if b_id != row['id']:
                relationships.append(
                    {'id_event1': row['id'], 'id_event2': b_id})

    return pd.DataFrame(relationships)


def event_to_location_relationship(events_entities: pd.DataFrame, location_entities,
                                   max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in tqdm(events_entities.iterrows(), total=events_entities.shape[0],
                           desc="Creating happened_in relationship", unit="row"):
        related_location_id = np.random.choice(location_entities['id'], 1,
                                               replace=False)
        relationships.append(
            {'id_event': row['id'], 'id_location': related_location_id[0]})
    return pd.DataFrame(relationships)


def object_to_location_to_person_to_event_relationship(object_entities: pd.DataFrame,
                                                       location_entities: pd.DataFrame,
                                                       person_entities: pd.DataFrame,
                                                       event_entities: pd.DataFrame):
    owns_relationship = []
    founded_in_relationship = []
    involved_in_relationship = []

    for index, row in tqdm(object_entities.iterrows(), total=object_entities.shape[0],
                           desc="Creating owns,involved_in,founded_in relationships",
                           unit="row"):

        # sceglie almeno una location random in cui l'oggetto
        location_id = np.random.choice(location_entities['id'], 1, replace=False)
        # stabilisce con una determinata probabilità se un oggetto è posseduto da una persona oppure no
        num_pers = np.random.choice([0, 1], p=[0.5, 0.5])
        people_id = []
        if num_pers != 0:
            people_id = np.random.choice(person_entities['id'], num_pers, replace=False)

        # seleziona nessuno o N eventi in cui l'oggetto corrente è coinvolto
        events_id = np.random.choice(event_entities['id'], np.random.randint(0, 4), replace=False)

        # assegna all'oggetto la location in cui è stato trovato
        founded_in_relationship.append(
            {'id_object': row['id'], 'id_location': location_id[0]})

        for person_id in people_id:
            owns_relationship.append(
                {'id_object': row['id'], 'id_person': person_id})

        for event_id in events_id:
            involved_in_relationship.append(
                {'id_object': row['id'], 'id_event': event_id})

    return pd.DataFrame(owns_relationship), pd.DataFrame(
        founded_in_relationship), pd.DataFrame(involved_in_relationship)
