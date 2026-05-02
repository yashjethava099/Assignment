# Write a Python function that takes a list and returns a new list with unique elements of the first list
def unique_list(lst):
    result = []
    
    for item in lst:
        if item not in result:
            result.append(item)
    
    return result

data = [1, 2, 2, 3, 4, 4, 5]

print("Unique list:", unique_list(data))