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
    ('occupation', lambda: fake.job())
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
    ("address", lambda: fake.address())
]
<<<<<<< HEAD

evidence_attributes = [
    ('evidence_type', lambda: random.choice(['DNA', 'Fingerprints', 'Blood'])),
    ('description', lambda: fake.sentence(nb_words=10)),
    ('date_collected', lambda: fake.date_between(start_date='-20y', end_date='today').isoformat()),
    ('status', lambda: random.choice(['Analyzed', 'Not Analyzed'])),
]

"""
Andiamo a definire  una serie di attributi per quattro categorie - persona,evento, oggetto luogo e prova.
--- PERSON ATTRIBUTES ---
Questa lista simula i dettagli di una persona, dove ogni elemento è una coppia composta da : 
1) Nome dell'attributo.
2) Funzione lambda che genera un valore per quell'attributo usando le librerie fake e random. In questo modo si ritarda l'esecuzione della funzione di faker
qinado viene chiamata la lambda.
Quindi sostanzialmetne abbiamo liste di tuple
"""
=======
>>>>>>> ludovico-branch
