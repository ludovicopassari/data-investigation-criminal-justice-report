from pathlib import Path
from data_generator import pd
# Imposta le opzioni per mostrare tutte le righe e colonne
pd.set_option('display.max_rows', None)  # Mostra tutte le righe
pd.set_option('display.max_columns', None)  # Mostra tutte le colonne
def generate_partition(data, percentage, dataset_dir, relationship_dir):

    people_entity_partition = pd.DataFrame(data['people'].iloc[:int(len(data['people']) * percentage)])
    people_entity_partition.to_csv(dataset_dir.joinpath('people_entity_partition_'+ str(int(percentage*100))+'.csv'), index=False)

    event_entity_partition = data['events'].iloc[:int(len(data['events']) * percentage)]
    event_entity_partition.to_csv(dataset_dir.joinpath('event_entity_partition_'+ str(int(percentage*100))+'.csv'), index=False)

    object_entity_partition = data['objects'].iloc[:int(len(data['objects']) * percentage)]
    object_entity_partition.to_csv(dataset_dir.joinpath('object_entity_partition_'+ str(int(percentage*100))+'.csv'), index=False)

    location_entity_partition = data['locations'].iloc[:int(len(data['locations']) * percentage)]
    location_entity_partition.to_csv(dataset_dir.joinpath('location_entity_partition_'+ str(int(percentage*100))+'.csv'), index=False)


    linked_to_person_p = pd.merge(people_entity_partition, data['linked_to'], left_on='id', right_on='id_person', how='inner')
    person_linked_to_event = pd.merge(linked_to_person_p, event_entity_partition, left_on='id_event', right_on='id',how='inner')
    linked_to_reduced = person_linked_to_event[['id_person', 'id_event']]
    linked_to_reduced.to_csv(relationship_dir.joinpath('linked_to_'+ str(int(percentage*100))+'.csv'), index=False)

    owns_person_p = pd.merge(people_entity_partition, data['owns'], left_on='id', right_on='id_person', how='inner')
    person_owns_object = pd.merge(owns_person_p, object_entity_partition, left_on='id_object', right_on='id',how='inner')
    owns_reduced = person_owns_object[['id_person', 'id_object']]
    owns_reduced.to_csv(relationship_dir.joinpath('owns_'+ str(int(percentage*100))+'.csv'), index=False)

    residence_in_person_p = pd.merge(people_entity_partition, data['residence_in'], left_on='id', right_on='id_person',how='inner')
    person_residence_in_location = pd.merge(residence_in_person_p, location_entity_partition, left_on='id_location',right_on='id', how='inner')
    residence_in_reduced = person_residence_in_location[['id_person', 'id_location']]
    residence_in_reduced.to_csv(relationship_dir.joinpath('residence_in_'+ str(int(percentage*100))+'.csv'), index=False)

    collaborate_with_person_p = pd.merge(people_entity_partition, data['collaborate_with'], left_on='id', right_on='id_person1',how='inner')
    person_collaborate_with_person = pd.merge(collaborate_with_person_p, people_entity_partition, left_on='id_person2',right_on='id', how='inner')
    collaborate_with_reduced = person_collaborate_with_person[['id_person1', 'id_person2']]
    collaborate_with_reduced.to_csv(relationship_dir.joinpath('collaborate_with_'+ str(int(percentage*100))+'.csv'), index=False)

    founded_in_object_p = pd.merge(object_entity_partition, data['founded_in'], left_on='id', right_on='id_object', how='inner')
    object_founded_in_location = pd.merge(founded_in_object_p, location_entity_partition, left_on='id_location',right_on='id', how='inner')
    founded_in_reduced = object_founded_in_location[['id_object', 'id_location']]
    founded_in_reduced.to_csv(relationship_dir.joinpath('founded_in_'+ str(int(percentage*100))+'.csv'), index=False)

    involved_in_object_p = pd.merge(object_entity_partition, data['involved_in'], left_on='id', right_on='id_object',how='inner')
    object_involved_in_event = pd.merge(involved_in_object_p, event_entity_partition, left_on='id_event', right_on='id',how='inner')
    involved_in_reduced = object_involved_in_event[['id_object', 'id_event']]
    involved_in_reduced.to_csv(relationship_dir.joinpath('involved_in_'+ str(int(percentage*100))+'.csv'), index=False)

    happened_in_event_p = pd.merge(event_entity_partition, data['happened_in'], left_on='id', right_on='id_event', how='inner')
    event_happened_in_location = pd.merge(happened_in_event_p, location_entity_partition, left_on='id_location',right_on='id', how='inner')
    happened_in_reduced = event_happened_in_location[['id_event', 'id_location']]
    happened_in_reduced.to_csv(relationship_dir.joinpath('happened_in_'+ str(int(percentage*100))+'.csv'), index=False)

    related_to_event_p = pd.merge(event_entity_partition, data['related_to'], left_on='id', right_on='id_event1', how='inner')
    event_related_to_event = pd.merge(related_to_event_p, event_entity_partition, left_on='id_event2', right_on='id',how='inner')
    collaborate_with_reduced = event_related_to_event[['id_event1', 'id_event2']]
    collaborate_with_reduced.to_csv(relationship_dir.joinpath('related_to_'+ str(int(percentage*100))+'.csv'), index=False)


def main():
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")
    relationship_dir = base_dir.joinpath("dataset", "relationships")

    data_100 = {
        'people' : pd.read_csv(dataset_dir.joinpath('people_data.csv')),
        'objects' : pd.read_csv(dataset_dir.joinpath('objects_data.csv')),
        'locations' : pd.read_csv(dataset_dir.joinpath('location_data.csv')),
        'events' : pd.read_csv(dataset_dir.joinpath('events_data.csv')),
        'linked_to' : pd.read_csv(relationship_dir.joinpath('linked_to.csv')),
        'owns' : pd.read_csv(relationship_dir.joinpath('owns.csv')),
        'related_to' : pd.read_csv(relationship_dir.joinpath('related_to.csv')),
        'residence_in' : pd.read_csv(relationship_dir.joinpath('residence_in.csv')),
        'involved_in' : pd.read_csv(relationship_dir.joinpath('involved_in.csv')),
        'happened_in' : pd.read_csv(relationship_dir.joinpath('happened_in.csv')),
        'founded_in' : pd.read_csv(relationship_dir.joinpath('founded_in.csv')),
        'collaborate_with' : pd.read_csv(relationship_dir.joinpath('collaborate_with.csv')),
    }


    generate_partition(data_100, 0.75, dataset_dir, relationship_dir)

    data_75 = {
        'people' : pd.read_csv(dataset_dir.joinpath('people_entity_partition_75.csv')),
        'objects' : pd.read_csv(dataset_dir.joinpath('object_entity_partition_75.csv')),
        'locations' : pd.read_csv(dataset_dir.joinpath('location_entity_partition_75.csv')),
        'events' : pd.read_csv(dataset_dir.joinpath('event_entity_partition_75.csv')),
        'linked_to' : pd.read_csv(relationship_dir.joinpath('linked_to_75.csv')),
        'owns' : pd.read_csv(relationship_dir.joinpath('owns_75.csv')),
        'related_to' : pd.read_csv(relationship_dir.joinpath('related_to_75.csv')),
        'residence_in' : pd.read_csv(relationship_dir.joinpath('residence_in_75.csv')),
        'involved_in' : pd.read_csv(relationship_dir.joinpath('involved_in_75.csv')),
        'happened_in' : pd.read_csv(relationship_dir.joinpath('happened_in_75.csv')),
        'founded_in' : pd.read_csv(relationship_dir.joinpath('founded_in_75.csv')),
        'collaborate_with' : pd.read_csv(relationship_dir.joinpath('collaborate_with_75.csv')),
    }

    generate_partition(data_75, 0.5, dataset_dir, relationship_dir)

    data_50 = {
        'people': pd.read_csv(dataset_dir.joinpath('people_entity_partition_50.csv')),
        'objects': pd.read_csv(dataset_dir.joinpath('object_entity_partition_50.csv')),
        'locations': pd.read_csv(dataset_dir.joinpath('location_entity_partition_50.csv')),
        'events': pd.read_csv(dataset_dir.joinpath('event_entity_partition_50.csv')),
        'linked_to': pd.read_csv(relationship_dir.joinpath('linked_to_50.csv')),
        'owns': pd.read_csv(relationship_dir.joinpath('owns_50.csv')),
        'related_to': pd.read_csv(relationship_dir.joinpath('related_to_50.csv')),
        'residence_in': pd.read_csv(relationship_dir.joinpath('residence_in_50.csv')),
        'involved_in': pd.read_csv(relationship_dir.joinpath('involved_in_50.csv')),
        'happened_in': pd.read_csv(relationship_dir.joinpath('happened_in_50.csv')),
        'founded_in': pd.read_csv(relationship_dir.joinpath('founded_in_50.csv')),
        'collaborate_with': pd.read_csv(relationship_dir.joinpath('collaborate_with_50.csv')),
    }
    generate_partition(data_50, 0.25, dataset_dir, relationship_dir)

if __name__ == '__main__':
    main()
