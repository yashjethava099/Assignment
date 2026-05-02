# Write a Python program to count occurrences of a substring in a string.

string = input("enter any string: ")
substring = input("enter any substring: ")
count = string.count(substring)
print(f"the substring {substring} occurs {count} times in the string {string}")