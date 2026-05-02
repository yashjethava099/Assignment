# Write a Python program to find the highest 3 values in a dictionary.

data = {"a": 10, "b": 45, "c": 23, "d": 67, "e": 34}
values = sorted(data.values(), reverse=True)
top3 = values[:3]
print("Top 3 values:", top3)