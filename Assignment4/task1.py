# Step 1: Create a dictionary of student names and marks
students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 88
}

# Step 2: Ask the user to input a student's name
name = input("Enter the student's name: ")

# Step 3 & 4: Retrieve marks or show 'not found' message
if name in students:
    print(f"{name}'s marks: {students[name]}")
else:
    print(f"Student '{name}' not found in the record.")
