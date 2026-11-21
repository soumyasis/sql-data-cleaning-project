import random
import pandas as pd
from faker import Faker
from pathlib import Path

random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

##writing the variables
NUM_CUSTOMERS = 200
NUM_ORDERS = 3000

##test print

print("Setup OK:", RAW_DIR)