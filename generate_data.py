import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)

rows = []

for i in range(500):

    age = np.random.randint(18, 60)
    income = np.random.randint(20000, 100000)

    # Younger customers prefer clothing
    if age < 30:
        category = np.random.choice(["Clothing", "Groceries"], p=[0.7, 0.3])
    else:
        category = np.random.choice(["Electronics", "Home Decor"], p=[0.6, 0.4])

    # Electronics are expensive
    if category == "Electronics":
        price = np.random.randint(3000, 10000)
    elif category == "Clothing":
        price = np.random.randint(500, 3000)
    else:
        price = np.random.randint(300, 4000)

    # Higher income buys more quantity
    if income > 60000:
        quantity = np.random.randint(2, 6)
    else:
        quantity = np.random.randint(1, 3)

    # Discounts increase quantity
    discount = np.random.choice(["Yes", "No"])
    if discount == "Yes":
        quantity += 1

    rows.append([
        i+1,
        age,
        np.random.choice(["Male", "Female"]),
        income,
        category,
        quantity,
        price,
        discount,
        pd.Timestamp("2024-01-01") + pd.Timedelta(days=i)
    ])

columns = [
    "Customer_ID",
    "Age",
    "Gender",
    "Income",
    "Product_Category",
    "Quantity",
    "Price",
    "Discount_Applied",
    "Purchase_Date"
]

df = pd.DataFrame(rows, columns=columns)
df.to_csv("data/customer_data.csv", index=False)

print("Smart dataset generated successfully!")
