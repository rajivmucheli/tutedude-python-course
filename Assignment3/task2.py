import math

# Asking user for a number
num = float(input("Enter a number: "))

# Calculations using math module
square_root = math.sqrt(num) if num >= 0 else "Undefined for negative numbers"
natural_log = math.log(num) if num > 0 else "Undefined for zero or negative numbers"
sine_value = math.sin(num)  # num is treated as radians

# Displaying results
print("\n--- Results ---")
print(f"Square root of {num}: {square_root}")
print(f"Natural logarithm (ln) of {num}: {natural_log}")
print(f"Sine of {num} (in radians): {sine_value}")
