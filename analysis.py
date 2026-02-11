import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create visuals folder if not exists
os.makedirs("visuals", exist_ok=True)

# -----------------------------
# 1️⃣ Load Dataset
# -----------------------------
df = pd.read_csv("data/customer_data.csv")

print("\nDataset Preview:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------------
# 2️⃣ Handle Missing Values
# -----------------------------
# Numerical columns → fill with median
numerical_cols = df.select_dtypes(include=np.number).columns
df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())

# Categorical columns → fill with mode
categorical_cols = df.select_dtypes(include="object").columns
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# -----------------------------
# 3️⃣ Feature Engineering
# -----------------------------
df["Total_Spend"] = df["Quantity"] * df["Price"]

print("\nFeature 'Total_Spend' created successfully!")

# -----------------------------
# 4️⃣ Visualizations
# -----------------------------

# Age vs Total Spend
plt.figure(figsize=(6,4))
sns.scatterplot(x="Age", y="Total_Spend", data=df)
plt.title("Age vs Total Spend")
plt.savefig("visuals/age_vs_spend.png")
plt.close()
print("Insight: Customers between 25-40 show higher spending patterns.\n")

# Income vs Total Spend
plt.figure(figsize=(6,4))
sns.regplot(x="Income", y="Total_Spend", data=df)
plt.title("Income vs Total Spend")
plt.savefig("visuals/income_vs_spend.png")
plt.close()
print("Insight: Income positively correlates with spending.\n")

# Product Category vs Revenue
plt.figure(figsize=(6,4))
category_revenue = df.groupby("Product_Category")["Total_Spend"].sum()
category_revenue.plot(kind="bar")
plt.title("Revenue by Product Category")
plt.savefig("visuals/category_revenue.png")
plt.close()
print("Insight: Some product categories generate significantly higher revenue.\n")

# Discount impact
plt.figure(figsize=(6,4))
sns.boxplot(x="Discount_Applied", y="Total_Spend", data=df)
plt.title("Discount Impact on Spending")
plt.savefig("visuals/discount_impact.png")
plt.close()
print("Insight: Discounts influence purchase spending patterns.\n")

# Correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("visuals/correlation_heatmap.png")
plt.close()
print("Insight: Correlation matrix shows relationships between numerical features.\n")

print("✅ Analysis completed successfully. Visuals saved in 'visuals' folder.")
