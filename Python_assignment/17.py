# Write a python program using function to find the sum of odd series and even series
def sum_even(n):
    total = 0
    for i in range(2, n+1, 2):
        total += i
    return total

def sum_odd(n):
    total = 0
    for i in range(1, n+1, 2):
        total += i
    return total

n = int(input("Enter a number: "))

even_sum = sum_even(n)
odd_sum = sum_odd(n)

print("Sum of even numbers:", even_sum)
print("Sum of odd numbers:", odd_sum)