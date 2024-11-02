from data_generator import fake, random

person_attributes = [
    ('first_name', lambda: fake.first_name()),
    ('last_name', lambda: fake.last_name()),
    ('gender', lambda: random.choice(['Male', 'Female'])),
    ('nationality', lambda: random.choice(['Italian', 'French', 'German', 'Spanish', 'English', 'American'])),
    ('relationship_status', lambda: random.choice(['Married', 'Single'])),
    ('phone_number', lambda: fake.phone_number()),
    ('email', lambda: fake.email()),
    ('date_of_birth', lambda: fake.date_of_birth(minimum_age=5, maximum_age=110)),
    ('occupation', lambda: random.choice(['Policeman', 'Engineer', "Doctor", "Workman"])),
    ('status', lambda: random.choice(['Suspected', 'Guilty', 'Innocent'])),
]

event_attributes = [
    ('event_type', lambda: random.choice(['Murder', 'Theft', 'Kidnapping', 'Attempt'])),
    ('description', lambda: fake.sentence(nb_words=10)),
    ("event_date", lambda: fake.date_between(start_date='-20y', end_date='today').isoformat()),
    ("status", lambda: random.choice(["Investigating", "Closed", "Pending"])),
    ('date_reported', lambda: fake.date_between(start_date='-20y', end_date='today').isoformat())
]

object_attributes = [
    ('type', lambda: random.choice(['Gun', 'Knife', 'Hammer', 'Ax'])),
    ('serial_number', lambda: fake.uuid4())
]

location_attributes = [
    ('latitude', lambda: fake.latitude()),
    ('longitude', lambda: fake.longitude()),
    ("street_name", lambda: fake.street_name()),
    ("building_number", lambda: fake.building_number()),
    ("city", lambda: fake.city()),
    ("state", lambda: fake.state()),
    ("country", lambda: fake.country()),
    ("postal_code", lambda: fake.postcode()),

]
