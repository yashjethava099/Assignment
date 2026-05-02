# Program to find Greatest Common Divisor of two numbers.For example, the GCD of 20 and 28 is 4 and GCD of 98 and 56 is 14.
def find_gcd(a, b):
    gcd = 1
    for i in range(1, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            gcd = i
    return gcd

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("GCD is:", find_gcd(num1, num2))