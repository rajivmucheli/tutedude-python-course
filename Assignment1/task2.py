# Program to create a personalized greeting message

# Taking user's first name and last name as input
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# Concatenating to form full name
full_name = first_name + " " + last_name

# Printing a personalized greeting
print(f"\nHello, {full_name}! Welcome!")
