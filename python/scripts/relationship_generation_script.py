from pathlib import Path
from data_generator import pd
from data_generator.relationship_generator import object_to_location_to_person_to_event_relationship, \
    person_to_event_relationship, person_to_person_relationship, event_to_location_relationship, \
    event_to_event_relationship, person_to_location


def main():
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")
    relationship_dir = base_dir.joinpath("dataset","relationships")
    print(relationship_dir)
    people = pd.read_csv(dataset_dir.joinpath("people_data.csv"))
    events = pd.read_csv(dataset_dir.joinpath("events_data.csv"))
    location_entities = pd.read_csv(dataset_dir.joinpath("location_data.csv"))
    object_entities = pd.read_csv(dataset_dir.joinpath("objects_data.csv"))

    owns, founded_in, involved_in = object_to_location_to_person_to_event_relationship(
        object_entities=object_entities,
        location_entities=location_entities,
        person_entities=people,
        event_entities=events)

    collaborate_with = person_to_person_relationship(people_entities=people)
    related_to = event_to_event_relationship(events_entities=events)
    linked_to = person_to_event_relationship(people_entities=people, event_entities=events)
    happened_in = event_to_location_relationship(events_entities=events, location_entities=location_entities)
    residence_in = person_to_location(people_entities=people, location_entities=location_entities)

    owns.to_csv(relationship_dir.joinpath("owns.csv"), index=True, index_label='id')
    founded_in.to_csv(relationship_dir.joinpath("founded_in.csv"), index=True, index_label='id')
    involved_in.to_csv(relationship_dir.joinpath("involved_in.csv"), index=True, index_label='id')
    collaborate_with.to_csv(relationship_dir.joinpath("collaborate_with.csv"), index=True, index_label='id')
    related_to.to_csv(relationship_dir.joinpath("related_to.csv"), index=True, index_label='id')
    linked_to.to_csv(relationship_dir.joinpath("linked_to.csv"), index=True, index_label='id')
    happened_in.to_csv(relationship_dir.joinpath("happened_in.csv"), index=True, index_label='id')
    residence_in.to_csv(relationship_dir.joinpath("residence_in.csv"), index=True, index_label='id')


if __name__ == '__main__':
    main()
