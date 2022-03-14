from cs50 import get_int

# Get input from user
while True:
    num = get_int("Number: ")
    if num >= 1 and num <= 8:
        break

# Print pyramid
row = 1
for i in range(num):  # to determine height
    for i in range(num - row):
        print(" ", end="")
    for i in range(row):
        print("#", end="")
    print("  ", end="")
    for i in range(row):
        print("#", end="")
    print("")
    row += 1
