# Import delle librerie necessarie
import pandas as pd
from faker import Faker
import random

from .generator import generate_data
from .generator_config import event_attributes, object_attributes, person_attributes, evidence_attributes, \
    location_attributes

# Creazione dell'istanza di Faker
fake = Faker()

# Esportazione delle librerie nel namespace del pacchetto
__all__ = ['pd', 'random', 'fake', 'event_attributes', 'object_attributes', 'person_attributes', 'evidence_attributes',
           'location_attributes']
