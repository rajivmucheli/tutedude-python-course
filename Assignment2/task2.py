def even(num1, num2):
    """Function to check whether two numbers are even or odd."""
    results = {}
    for num in (num1, num2):
        if num % 2 == 0:
            results[num] = "even"
        else:
            results[num] = "odd"
    return results

def odd(num1, num2):
    """Function to check whether two numbers are odd or even."""
    results = {}
    for num in (num1, num2):
        if num % 2 != 0:
            results[num] = "odd"
        else:
            results[num] = "even"
    return results

even(4, 7)
odd(3, 8)