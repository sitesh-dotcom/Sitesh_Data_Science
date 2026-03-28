import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the dataset
df = sns.load_dataset('titanic')
# 6. Print the first 5 rows to see the data
# 7. Calculate and print the survival rate
survival_count = df['survived'].value_counts()
survival_rate = df['survived'].mean() * 100

print(f"\n--- Survival Stats ---")
print(f"Number of survivors: {survival_count[1]}")
print(f"Number of deaths: {survival_count[0]}")
print(f"Overall Survival Rate: {survival_rate:.2f}%")
print("\n--- Titanic Dataset Preview ---")
print(df.head())
# 2. Select only the numerical columns (Correlation only works on numbers)
numerical_df = df.select_dtypes(include=['float64', 'int64'])

# 3. Calculate the correlation matrix
corr_matrix = numerical_df.corr()

# 4. Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")

# 5. Add a title and show it
plt.title('Correlation Heatmap: Titanic Dataset')
plt.savefig('my_heatmap.png')






