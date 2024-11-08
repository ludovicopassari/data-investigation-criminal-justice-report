from data_generator import pd
from pathlib import Path
import json


def generate_person_documents(people,df_residence_in,df_linked_to,collaborate_with):
    people_collection = {}
    not_inserted_yet = {}

    for index, row in people.iterrows():
        curr_person_id = row['id_person']

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

        if curr_person_id in df_residence_in['id_person'].values:
            curr = df_residence_in[df_residence_in['id_person'] == curr_person_id]

            persona["residence"] = {
                "street_name": df_residence_in[df_residence_in['id_person'] == curr_person_id]['street_name'].item(),
                "building_number": df_residence_in[df_residence_in['id_person'] == curr_person_id][
                    'building_number'].item(),
                "city": df_residence_in[df_residence_in['id_person'] == curr_person_id]['city'].item(),
                "state": df_residence_in[df_residence_in['id_person'] == curr_person_id]['state'].item(),
                "country": df_residence_in[df_residence_in['id_person'] == curr_person_id]['country'].item(),
                "postal_code": df_residence_in[df_residence_in['id_person'] == curr_person_id]['postal_code'].item(),
            }

        if curr_person_id in df_linked_to['id_person'].values:
            persona["involved_in"] = df_linked_to[df_linked_to['id_person'] == curr_person_id][
                'id_event'].values.tolist()

        if curr_person_id in collaborate_with['id_person1'].values:
            people_collaborate_with = collaborate_with[collaborate_with['id_person1'] == curr_person_id][
                'id_person2'].values.tolist()
            persona["collaborate_with"] = people_collaborate_with

            not_inserted_yet[curr_person_id] = people_collaborate_with

        people_collection[curr_person_id] = persona

    for id, list_people in not_inserted_yet.items():
        for _ in list_people:
            people_collection[_]['collaborate_with'].append(id)

    with open('people_collection.json', 'w') as f:
        for record in list(people_collection.values()):
            # Converti ogni dizionario in una stringa JSON e scrivilo su una nuova riga
            f.write(json.dumps(record) + "\n")



def main():
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")

    people = pd.read_csv(dataset_dir.joinpath("people_data.csv"))
    people.rename(columns={'id': 'id_person'}, inplace=True)

    events = pd.read_csv(dataset_dir.joinpath("events_data.csv"))
    events.rename(columns={'id': 'id_event'}, inplace=True)

    location_entities = pd.read_csv(dataset_dir.joinpath("location_data.csv"))
    location_entities.rename(columns={'id': 'id_location'}, inplace=True)
    object_entities = pd.read_csv(dataset_dir.joinpath("objects_data.csv"))

    residence_in = pd.read_csv(dataset_dir.joinpath("residence_in.csv"))
    linked_to = pd.read_csv(dataset_dir.joinpath("linked_to.csv"))
    collaborate_with = pd.read_csv(dataset_dir.joinpath("collaborate_with.csv"))

    df_partial_join_linked_to = pd.merge(linked_to, people, on='id_person', how='left')
    df_linked_to = pd.merge(df_partial_join_linked_to, events, on='id_event', how='left')

    df_partial_join_residence_in = pd.merge(residence_in, people, on='id_person', how='left')
    df_residence_in = pd.merge(df_partial_join_residence_in, location_entities, on='id_location', how='left')

    generate_person_documents(people, df_residence_in,df_linked_to,collaborate_with)

if __name__ == '__main__':
    main()

