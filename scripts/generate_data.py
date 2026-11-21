import random
import pandas as pd
from faker import Faker
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Settings
NUM_CUSTOMERS = 200
NUM_ORDERS = 3000

CITIES = [
    "Kolkata", "Delhi", "Mumbai", "Chennai", "Bengaluru",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna",
    "Surat", "Vadodara", "Guwahati", "Bhubaneswar", "Chandigarh",
]

MALE_NAMES = [
    "Rahul", "Amit", "Sourav", "Arjun", "Rohan", "Debashis", "Vikram",
    "Sandeep", "Anirban", "Kunal", "Rajesh", "Suresh", "Abhishek", "Subhajit",
    "Manish", "Pranav", "Aditya", "Sumit", "Tanmoy", "Nikhil",
    "Ravi", "Gaurav", "Sanjay", "Partha", "Ayan",
]

FEMALE_NAMES = [
    "Priya", "Ananya", "Sneha", "Riya", "Pooja", "Debjani", "Neha",
    "Kavita", "Moumita", "Isha", "Sunita", "Anjali", "Shreya", "Puja",
    "Swati", "Meera", "Nandini", "Tanvi", "Sayani", "Rupa",
    "Divya", "Komal", "Payel", "Aditi", "Sonali",
]

LAST_NAMES = [
    "Sharma", "Das", "Banerjee", "Singh", "Gupta", "Mukherjee", "Patel",
    "Roy", "Verma", "Chatterjee", "Ghosh", "Sen", "Bose", "Jain",
    "Agarwal", "Mehta", "Kumar", "Yadav", "Mishra", "Dutta",
    "Saha", "Pal", "Nair", "Reddy", "Kapoor",
]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

# Stage 2: customers (clean)
customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    sex = random.choice(["M", "F"])

    if sex == "M":
        first_name = random.choice(MALE_NAMES)
    else:
        first_name = random.choice(FEMALE_NAMES)

    if random.random() < 0.4:
        if sex == "M":
            middle_name = random.choice(MALE_NAMES)
        else:
            middle_name = random.choice(FEMALE_NAMES)
    else:
        middle_name = None

    last_name = random.choice(LAST_NAMES)

    email = (
        f"{first_name.lower()}.{last_name.lower()}"
        f"{random.randint(1, 99)}@{random.choice(EMAIL_DOMAINS)}"
    )

    customers.append({
        "customer_id": f"C{i:03d}",
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "sex": sex,
        "date_of_birth": fake.date_of_birth(minimum_age=22, maximum_age=70),
        "email": email,
        "city": random.choice(CITIES),
        "segment": random.choice(["Premium", "Regular", "Basic"]),
        "signup_date": fake.date_between(start_date="-3y", end_date="-1y"),
    })

customers_df = pd.DataFrame(customers)

print(customers_df.head())
print(len(customers_df))