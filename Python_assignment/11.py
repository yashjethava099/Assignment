# Write a Python program to unzip a list of tuples into individual lists.
data = [(1, 2), (3, 4), (5, 6)]

# Unzip
list1, list2 = zip(*data)

# Convert to list (optional)
list1 = list(list1)
list2 = list(list2)

print("List 1:", list1)
print("List 2:", list2)