# num1 = 100
# num2 = 200
# num1,num2 = 100,200
num1 = num2 = 200
add = num1 + num2
print("addition ", add)
print(type (add))
msg = """
ml = machne learning
dl = deep learning
NLP = natural language processing
Gen AI = Generative AI
"""
print(msg)
print(type(msg))
flag1 = True
flag2 = False
print(flag1)
print(flag2)
print(type(flag1))
age = 20
flag1 = age > 18
print(flag1)
numbers = [100,200,300,400,500]
print(numbers[0],numbers[-5])
print(type(numbers))
numbers[0] = 111
print(numbers)
import pandas as pd
import numpy as np

# Create a small dataset to test
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Score': [85, 92, 78]
}

df = pd.DataFrame(data)

print("--- Data Science Environment Active ---")
print(df)
print("\nAverage Score:", df['Score'].mean())
import seaborn as sns
import pandas as pd

# Load the classic Titanic dataset
df = sns.load_dataset('titanic')

# Display the first 5 rows
print("--- Titanic Dataset Loaded ---")
print(df.head())

# Quick Analysis: What was the survival rate by gender?
print("\nSurvival Rate by Gender:")
print(df.groupby('sex')['survived'].mean())
x = 2323
y = 2323
print(x is y)



