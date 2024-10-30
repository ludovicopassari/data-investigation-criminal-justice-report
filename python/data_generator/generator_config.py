from data_generator import fake, random

person_attributes = [
    ('first_name', lambda: fake.first_name()),
    ('last_name', lambda: fake.last_name()),
    ('gender', lambda: random.choice(['Male', 'Female'])),
    ('nationality', lambda: random.choice(['Italian', 'French', 'German', 'Spanish', 'English', 'American'])),
    ('relationship_status', lambda: random.choice(['Married', 'Single'])),
    ('phone_number', lambda: fake.phone_number()),
    ('email', lambda: fake.email()),
    ('phone_number', lambda: fake.phone_number()),
    ('date_of_birth', lambda: fake.date_of_birth(minimum_age=5, maximum_age=110)),
    ('occupation', lambda: fake.job())
]

event_attributes = [
    ('event_type', lambda: random.choice(['Omicidio', 'Furto'])),
    ('description', lambda: fake.sentence(nb_words=10)),
    ("event_date", lambda: fake.date_between(start_date='-20y', end_date='today').isoformat()),
    ("status", lambda: random.choice(["Investigating", "Closed", "Pending"])),
    ('date_reported', lambda: fake.date_between(start_date='-20y', end_date='today').isoformat())
]


object_attributes = [
    ('type', lambda: random.choice(['Weapon', 'Knife'])),
    ('serial_number', lambda: fake.uuid4()),

]

location_attributes = [
    ('type', lambda: random.choice(['Street Address', 'Residence'])),
    ('latitude', lambda: fake.latitude()),
    ('longitude', lambda: fake.longitude()),
    ("address", lambda: fake.address())
]

evidence_attributes = [
    ('evidence_type', lambda: random.choice(['DNA', 'Fingerprints', 'Blood'])),
    ('description', lambda: fake.sentence(nb_words=10)),
    ('date_collected', lambda: fake.date_between(start_date='-20y', end_date='today').isoformat()),
    ('status', lambda: random.choice(['Analyzed', 'Not Analyzed'])),
]
