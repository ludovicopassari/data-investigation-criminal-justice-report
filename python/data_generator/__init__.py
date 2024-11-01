# Import delle librerie necessarie
import pandas as pd
from faker import Faker
import random
from .generator import generate_data


# Creazione dell'istanza di Faker
fake = Faker()

# Esportazione delle librerie nel namespace del pacchetto
__all__ = ['pd', 'random', 'fake', 'generate_data']


"""
In questo script abbiamo importato le librerie utili, creato un'istanza di faker e
definito quali elementi deovno essere accessibili da altri moduli che importano questo
pacchetto. 
__all__ = è una lista che specifica quali nomi devono essere esportati quando si utilizza l'istruzione
form module import *. In altre parole quando un altro modulo importa tutto dal modulo corrente, solo gli oggetti
elencati in __all__ saranno accessibili.
"""