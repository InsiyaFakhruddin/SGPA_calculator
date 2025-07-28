import pandas as pd

# Define the LUMS grading data
lums_data = {
    "Grade": ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"],
    "GPA": [4.00, 3.70, 3.30, 3.00, 2.70, 2.30, 2.00, 1.70, 1.00, 0.00],
    "Min Marks": [90, 85, 80, 75, 70, 65, 60, 55, 50, 0],
    "Max Marks": [100, 89, 84, 79, 74, 69, 64, 59, 54, 49]
}

# Create DataFrame
df = pd.DataFrame(lums_data)

# Save to Excel
df.to_excel("LUMS.xlsx", index=False)

print("✅ LUMS.xlsx has been created successfully.")
