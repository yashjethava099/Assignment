# Given a number n, write a python program to make and print the list of Fibonacci series up to n.
n = int(input("Enter n: "))

fib = [0, 1]

for i in range(2, n+1):
    fib.append(fib[i-1] + fib[i-2])

print("First few Fibonacci numbers are:", fib)