# Write a python program to sum of the first n positive integers.

n = int(input("enter n number "))
total = 0
for i in range(1, n+1):
    total += i
print(f"first positive {n} sum is {total}")