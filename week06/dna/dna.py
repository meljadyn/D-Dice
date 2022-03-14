import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: dna.py file.csv file.txt")
    data = sys.argv[1]
    sequence = sys.argv[2]

    # Read database file into a variable
    dna_match = []  # to be a list of lists, with dna_match[1] being the key
    with open(data, "r") as file:
        reader = csv.DictReader(file)
        dna_match = list(reader)  # Source: [1] AMC on StackOverflow (see link at bottom of file)

    # Read DNA sequence file into a variable
    with open(sequence, "r") as file:
        seq = file.read()

    # // Find longest match of each STR in DNA sequence
    # Isolate DNA STRs in separate list
    str_types = []

    # Copy the header list from my list of lists
    str_types = list(dna_match[0])

    # Remove first element of that list
    str_types.pop(0)

    # // Save the DNA sequence numbers in a list
    match_list = []  # number of DNA matches
    for i in range(len(str_types)):  # The length of all listed DNA types in the key
        match = longest_match(seq, str_types[i])  # Saves # of consecutive matches in a list
        match_list.append(match)

    # // Compare the DNA sequence list to each participant
    for i in range(len(dna_match)):  # Go for the number of participants
        counter = 0
        for j in range(len(str_types)):  # number of DNA types
            # If the DNA # matches the dna type for this person
            if str(match_list[j]) == str(dna_match[i][str_types[j]]):
                counter += 1

        # if the counter total is equal to the number of DNA types, we have found a match!
        if counter == len(str_types):
            print(f"{dna_match[i]['name']}")
            return 0

    # If the program reaches this point, then no matches were found
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()


# SOURCE LIST
# to help convert a csv input to list
# [1] https://stackoverflow.com/questions/24662571/python-import-csv-to-list