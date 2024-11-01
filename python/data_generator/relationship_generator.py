from data_generator import random
from data_generator import pd
import numpy as np


def person_to_event_relationship(people_entities: pd.DataFrame, event_entities: pd.DataFrame,
                                 max_relationship=3) -> pd.DataFrame:
    relationships = []

    for index, row in people_entities.iterrows():
        num_relationships = np.random.randint(0, max_relationship + 1)
        related_b = np.random.choice(event_entities['id'], num_relationships, replace=False)

        for b_id in related_b:
            relationships.append({'id_person': row['id'], 'id_event': b_id})

    return pd.DataFrame(relationships)


def person_to_person(people_entities: pd.DataFrame, max_relationship=3):
    relationships = []

    for index, row in people_entities.iterrows():
        num_relationships = np.random.randint(0, max_relationship + 1)
        related_b = np.random.choice(people_entities['id'], num_relationships, replace=False)

        for b_id in related_b:
            relationships.append({'id_person1': row['id'], 'id_person2': b_id})

    return pd.DataFrame(relationships)


def person_to_location(people_entities: pd.DataFrame, location_entities: pd.DataFrame):
   residence_in = []
   for index,row in people_entities.iterrows():
       location_id = []
       has_home = np.random.choice([0,1],p=[0.8,0.2])
       if has_home:
           location_id = np.random.choice(location_entities['id'],has_home)
       for id in location_id:
           residence_in.append({'id_person': row['id'], 'id_location': id})
   df=pd.DataFrame(residence_in)
   return df

def main():
    people = pd.read_csv(
        '/Users/mattiamusarra/Desktop/ProgettoDBNoSql/data-investigation-criminal-justice-report/dataset/people_data.csv')
    events = pd.read_csv(
        '/Users/mattiamusarra/Desktop/ProgettoDBNoSql/data-investigation-criminal-justice-report/dataset/events_data.csv')
    object=pd.read_csv('/Users/mattiamusarra/Desktop/ProgettoDBNoSql/data-investigation-criminal-justice-report/dataset/objects_data.csv')
    location=pd.read_csv('/Users/mattiamusarra/Desktop/ProgettoDBNoSql/data-investigation-criminal-justice-report/dataset/location_data.csv')

    locationToPerson=person_to_location(people,location)
    print(locationToPerson)
if __name__ == '__main__':
    main()