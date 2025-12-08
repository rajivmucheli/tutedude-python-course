# Step 1: Take user input and write it to output.txt
user_text = input("Enter text to write to the file: ")

with open("output.txt", "w") as file:
    file.write(user_text + "\n")

# Step 2: Append additional data to the same file
append_text = input("Enter additional text to append: ")

with open("output.txt", "a") as file:
    file.write(append_text + "\n")

# Step 3: Read and display the final content of the file
print("\n--- Final Content of output.txt ---")

with open("output.txt", "r") as file:
    content = file.read()
    print(content)
