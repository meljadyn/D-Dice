# A program that asks for your name to greet you appropriately.

from cs50 import get_string

name = get_string("What is your name? ")
print(f"hello, {name}")