# Write a Python program to sort a dictionary (ascending /descending) by value.
data = {"a": 3, "b": 1, "c": 2}

Ascending = dict(sorted(data.items(), key=lambda x: x[1]))
Descending = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
print("Ascending:", Ascending)
print("Descending:", Descending)