from data_generator import pd
import numpy as np


# function
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


def main():
    people = pd.read_csv(
        '/Users/vico/Documents/projects/uni_prj/db/data-investigation-criminal-justice-report/dataset/people_data.csv')
    events = pd.read_csv(
        '/Users/vico/Documents/projects/uni_prj/db/data-investigation-criminal-justice-report/dataset/events_data.csv')

    persons = person_to_person(people, max_relationship=3)
    print(persons)


if __name__ == '__main__':
    main()
