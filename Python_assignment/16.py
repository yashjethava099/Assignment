# Counting the frequencies in a list using a dictionary in Python.

data = [1, 1, 1, 5, 5, 3, 1, 3, 3, 1, 4, 4, 4, 2, 2, 2, 2]

freq = {}

for num in data:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

# Print in sorted order
for key in sorted(freq):
    print(key, ":", freq[key], end=" , ")