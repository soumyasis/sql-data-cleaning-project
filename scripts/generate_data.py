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

PRODUCTS = {
    # Computer accessories
    "Mouse": (300, 1500),
    "Keyboard": (500, 3000),
    "Webcam": (1200, 4500),
    "USB Cable": (100, 500),
    "Laptop Bag": (600, 3000),
    "Mouse Pad": (150, 800),
    "USB Hub": (400, 2000),
    "Pen Drive 64GB": (400, 1000),
    "External Hard Drive": (3500, 8000),
    "Laptop Stand": (700, 3000),

    # Audio
    "Headphones": (800, 5000),
    "Bluetooth Speaker": (1000, 8000),
    "Earbuds": (500, 6000),
    "Soundbar": (4000, 20000),
    "Microphone": (1000, 7000),

    # Mobile accessories
    "Power Bank": (700, 3500),
    "Phone Case": (150, 1200),
    "Screen Guard": (100, 600),
    "Phone Charger": (300, 2000),
    "Selfie Stick": (300, 1500),

    # Electronics and appliances
    "Monitor": (7000, 20000),
    "Smart Watch": (1500, 15000),
    "Fitness Band": (1200, 5000),
    "Tablet": (8000, 35000),
    "Printer": (4500, 18000),
    "Wi-Fi Router": (1000, 6000),
    "Table Lamp": (400, 2500),
    "Electric Kettle": (600, 2500),
    "Air Fryer": (3500, 10000),
    "Mixer Grinder": (2000, 6500),

    # Home and office
    "Office Chair": (3500, 15000),
    "Study Desk": (3000, 12000),
    "Notebook Pack": (150, 700),
    "Backpack": (800, 4000),
    "Water Bottle": (200, 1200),

    # Gaming
    "Gaming Mouse": (800, 5000),
    "Gaming Keyboard": (1500, 8000),
    "Game Controller": (1500, 6000),
    "Gaming Headset": (1500, 7000),
    "Mousepad XL": (500, 2500),
}

# Stage 2: customers (clean data)
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
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70),
        "email": email,
        "city": random.choice(CITIES),
        "segment": random.choice(["Premium", "Regular", "Basic"]),
        "signup_date": fake.date_between(start_date="-3y", end_date="-1y"),
    })

customers_df = pd.DataFrame(customers)

# Stage 3: orders (clean)

active_customers = customers[:int(NUM_CUSTOMERS * 0.9)]  # last 10% never order

orders = []

for i in range(NUM_ORDERS):
    c = random.choice(active_customers)
    product = random.choice(list(PRODUCTS))
    low, high = PRODUCTS[product]

    orders.append({
        "order_id": 1001 + i,
        "customer_id": c["customer_id"],
        "product": product,
        "quantity": random.randint(1, 20),
        "unit_price": round(random.uniform(low, high), 2),
        "order_date": fake.date_between(start_date=c["signup_date"], end_date="today"),
    })

orders_df = pd.DataFrame(orders)

# ---------------------------------------------------------------
# Stage 4A: mess up customers
# ---------------------------------------------------------------
# Extra spaces (15% of first names, 15% of last names)
idx = customers_df.sample(frac=0.15, random_state=1).index
customers_df.loc[idx, "first_name"] = "  " + customers_df.loc[idx, "first_name"] + " "

idx = customers_df.sample(frac=0.15, random_state=2).index
customers_df.loc[idx, "last_name"] = " " + customers_df.loc[idx, "last_name"] + "  "

# Mixed case
idx = customers_df.sample(frac=0.20, random_state=3).index
customers_df.loc[idx, "last_name"] = customers_df.loc[idx, "last_name"].str.upper()

idx = customers_df.sample(frac=0.20, random_state=4).index
customers_df.loc[idx, "first_name"] = customers_df.loc[idx, "first_name"].str.lower()

idx = customers_df.sample(frac=0.20, random_state=5).index
customers_df.loc[idx, "city"] = customers_df.loc[idx, "city"].str.upper()

idx = customers_df.sample(frac=0.10, random_state=6).index
customers_df.loc[idx, "city"] = customers_df.loc[idx, "city"].str.lower()

# Inconsistent sex codes (25%)
idx = customers_df.sample(frac=0.25, random_state=7).index
customers_df.loc[idx, "sex"] = customers_df.loc[idx, "sex"].apply(
    lambda x: random.choice(["Male", "male", "m"]) if x == "M"
    else random.choice(["Female", "female", "f"])
)

# Uppercase emails (10%)
idx = customers_df.sample(frac=0.10, random_state=8).index
customers_df.loc[idx, "email"] = customers_df.loc[idx, "email"].str.upper()

# Duplicate customers (3%) - always last
dupes = customers_df.sample(frac=0.03, random_state=9)
customers_df = pd.concat([customers_df, dupes], ignore_index=True)
customers_df = customers_df.sample(frac=1, random_state=10).reset_index(drop=True)

# ---------------------------------------------------------------
# Stage 4B: mess up orders
# ---------------------------------------------------------------
# Blank quantity (None -> NULL) and blank price (empty string)
orders_df["quantity"] = orders_df["quantity"].astype(object)
orders_df["unit_price"] = orders_df["unit_price"].astype(object)

idx = orders_df.sample(frac=0.05, random_state=11).index
orders_df.loc[idx, "quantity"] = None

idx = orders_df.sample(frac=0.05, random_state=12).index
orders_df.loc[idx, "unit_price"] = ""

# Orphan customer IDs (5%) - these IDs are not in the master file
idx = orders_df.sample(frac=0.05, random_state=13).index
orders_df.loc[idx, "customer_id"] = [
    random.choice(["C999", "C998", "C997", "C950"]) for _ in idx
]

# Duplicate orders (5%) - always last
dupes = orders_df.sample(frac=0.05, random_state=14)
orders_df = pd.concat([orders_df, dupes], ignore_index=True)
orders_df = orders_df.sample(frac=1, random_state=15).reset_index(drop=True)


# Stage 5: save CSVs

RAW_DIR.mkdir(parents=True, exist_ok=True)

customers_df.to_csv(RAW_DIR / "customers_master.csv", index=False)
orders_df.to_csv(RAW_DIR / "orders_raw.csv", index=False)


# Stage 6: summary ( numbers for my README)

print(customers_df.head())
print(orders_df.head())
print()
print("Customers rows:", len(customers_df))
print("Duplicate customers:", customers_df.duplicated().sum())
print("Blank middle names:", customers_df["middle_name"].isna().sum())
print()
print("Orders rows:           ", len(orders_df))
print("Duplicate orders:      ", orders_df.duplicated().sum())
print("Blank quantity:        ", orders_df["quantity"].isna().sum())
print("Blank unit_price:      ", (orders_df["unit_price"] == "").sum())
print("Orphan orders:         ",
      (~orders_df["customer_id"].isin(customers_df["customer_id"])).sum())
print("Customers who never ordered:",
      (~customers_df["customer_id"].drop_duplicates()
       .isin(orders_df["customer_id"])).sum())
print()
print("Saved to:", RAW_DIR)