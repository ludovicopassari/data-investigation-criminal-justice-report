# Import delle librerie necessarie
import pandas as pd
from faker import Faker
import random
from .generator import generate_data


# Creazione dell'istanza di Faker
fake = Faker()

# Esportazione delle librerie nel namespace del pacchetto
__all__ = ['pd', 'random', 'fake', 'generate_data']
