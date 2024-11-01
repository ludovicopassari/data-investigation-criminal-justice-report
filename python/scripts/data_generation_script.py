from data_generator.generator_config import person_attributes, object_attributes, event_attributes, location_attributes
from data_generator import generate_data
from pathlib import Path

# Ottenere il percorso del file Python in esecuzione
current_file_path = Path(__file__).resolve()

# Ottenere la directory corrente
output_path = current_file_path.parent.parent.parent.joinpath('dataset')

people_path = output_path.joinpath('people_data.csv')
events_path = output_path.joinpath('events_data.csv')
objects_path = output_path.joinpath('objects_data.csv')
location_path = output_path.joinpath('location_data.csv')
# evidence_path = output_path.joinpath('evidence_data.csv')

people = generate_data(100000, person_attributes, 'csv', people_path)
events = generate_data(20000, event_attributes, 'csv', events_path)
objects = generate_data(50000, object_attributes, 'csv', objects_path)
location = generate_data(20000, location_attributes, 'csv', location_path)


