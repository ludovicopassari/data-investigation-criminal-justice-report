from data_generator import pd
import numpy as np
import random
from typing import Tuple
import os
from pathlib import Path


def person_to_event_relationship(people_entities: pd.DataFrame,
                                 event_entities: pd.DataFrame,
                                 max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in people_entities.iterrows():
        num_relationships = np.random.randint(0, max_relationship + 1)
        related_b = np.random.choice(event_entities['id'], num_relationships,
                                     replace=False)

        for b_id in related_b:
            relationships.append({'id_person': row['id'], 'id_event': b_id})

    return pd.DataFrame(relationships)


def person_to_person_relationship(people_entities: pd.DataFrame, max_relationship=3):
    relationships = []

    for index, row in people_entities.iterrows():
        # specifica quante persone devono essere messe in relazione con la persona corrente
        num_relationships = np.random.randint(0, max_relationship + 1)
        # estrae in maniera random un numero di 'id' di persone pari a 'num_relationship' dal dataframe delle le persone
        related_b = np.random.choice(people_entities['id'], num_relationships,
                                     replace=False)
        # per ogni persona estratta verifica che essa non sia messa in relazione con se stessa
        for b_id in related_b:
            if b_id != row['id']:
                relationships.append(
                    {'id_person1': row['id'], 'id_person2': b_id})

    return pd.DataFrame(relationships)


def event_to_event_relationship(events_entities: pd.DataFrame, max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in events_entities.iterrows():
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

    for index, row in events_entities.iterrows():
        related_location_id = np.random.choice(location_entities['id'], 1,
                                               replace=False)
        relationships.append(
            {'id_event1': row['id'], 'id_location': related_location_id[0]})
    return pd.DataFrame(relationships)


def object_to_location_to_person_to_event_relationship(object_entities: pd.DataFrame,
                                                       location_entities: pd.DataFrame,
                                                       person_entities: pd.DataFrame,
                                                       event_entities: pd.DataFrame):
    owns_relationship = []
    founded_in_relationship = []
    involved_in_relationship = []

    for index, row in object_entities.iterrows():
        # un oggetto è posseduto da una persona o da nessuno
        person = []
        # un oggetto può essere coinvolto in nessuno o in molti eventi
        events = []
        # un oggetto deve essere trovato in una location
        location = []

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
            {'object_id': row['id'], 'location_id': location_id[0]})

        for person_id in people_id:
            owns_relationship.append(
                {'object_id': row['id'], 'person_id': person_id})

        for event_id in events_id:
            involved_in_relationship.append(
                {'object_id': row['id'], 'event_id': event_id})

    return pd.DataFrame(owns_relationship), pd.DataFrame(
        founded_in_relationship), pd.DataFrame(involved_in_relationship)


def main():
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")

    people = pd.read_csv(dataset_dir.joinpath("people_data.csv"))
    events = pd.read_csv(dataset_dir.joinpath("events_data.csv"))
    location_entities = pd.read_csv(dataset_dir.joinpath("location_data.csv"))
    object_entities = pd.read_csv(dataset_dir.joinpath("objects_data.csv"))

    owns, founded, involved = object_to_location_to_person_to_event_relationship(
        object_entities=object_entities,
        location_entities=location_entities,
        person_entities=people,
        event_entities=events)


if __name__ == '__main__':
    main()
