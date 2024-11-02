from data_generator import pd
from pathlib import Path


def main():
    base_dir = Path(__file__).parent.parent.parent
    dataset_dir = base_dir.joinpath("dataset", "")

    people = pd.read_csv(dataset_dir.joinpath("people_data.csv"))
    people.rename(columns={'id': 'id_person'}, inplace=True)

    events = pd.read_csv(dataset_dir.joinpath("events_data.csv"))
    location_entities = pd.read_csv(dataset_dir.joinpath("location_data.csv"))
    location_entities.rename(columns={'id': 'id_location'}, inplace=True)
    object_entities = pd.read_csv(dataset_dir.joinpath("objects_data.csv"))

    residence_in = pd.read_csv(dataset_dir.joinpath("residence_in.csv"))
    involved_in = pd.read_csv(dataset_dir.joinpath("involved_in.csv"))
    collaborate_with = pd.read_csv(dataset_dir.joinpath("location_data.csv"))

    df_join1 = pd.merge(residence_in, people, on='id_person', how='left')
    df_finale = pd.merge(df_join1, location_entities, on='id_location', how='left')

    print(df_join1.head(20))

    df_finale.to_csv(base_dir.joinpath("join.csv"), index=False)


if __name__ == '__main__':
    main()
