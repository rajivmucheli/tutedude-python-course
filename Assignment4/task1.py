# Program to read a file line by line with error handling

try:
    with open("sample.txt", "r") as file:
        print("Contents of sample.txt:\n")
        for line in file:
            print(line.strip())  # strip() removes the newline character
except FileNotFoundError:
    print("Error: The file 'sample.txt' does not exist.")
except Exception as e:
    print("An unexpected error occurred:", e)
