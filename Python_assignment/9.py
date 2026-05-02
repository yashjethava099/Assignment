# Write a Python program to find the second smallest number in a list. 
numbers = [5, 20, 8, 1, 3]

# Remove duplicates and sort
numbers = list(set(numbers))
numbers.sort()

# Second smallest
print("Second smallest number is:", numbers[1])