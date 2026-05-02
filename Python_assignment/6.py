# Write a Python program to find the first appearance of the substring 'not' and 'poor' from a given string, if 'not' follows the 'poor', replace the whole 'not'...'poor' substring with 'good'. Return the resulting string
# s = input("enter string")
# not_index = s.find("not")
# poor_index = s.find("poor")
# print(not_index)
# print(poor_index)

def replace_not_poor(s):
    not_index = s.find("not")
    poor_index = s.find("poor")

    if not_index != -1 and poor_index != -1 and poor_index > not_index:
        return s[:not_index] + "good" + s[poor_index + 4:]
    else:
        return s

# Input
text = input("Enter a string: ")

# Output
print("Result:", replace_not_poor(text))