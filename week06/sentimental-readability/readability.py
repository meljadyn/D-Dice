from cs50 import get_string


def main():
    # Get text with get_string
    text = get_string("Text: ")

    # Count letters (a-z, A-Z)
    letters = count_letters(text)

    # Count words (any sequence of character separated by a space)
    words = count_words(text)

    # Count sentences (marked by . ! ?)
    sentences = count_sentences(text)

    # Print Grade X (X = Grade Level)
    grade = grade_level(letters, words, sentences)

    if grade < 1:
        print("Before Grade 1")
        return 0
    if grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def count_letters(text):
    count = 0  # Variable to store number of spaces
    for i in range(len(text)):
        if text[i].isalpha() == True:
            count += 1

    return count


def count_words(text):
    count = 1  # Start a 1 because the lat word of a string will not end in a space
    for i in range(len(text)):
        if text[i].isspace() == True:
            count += 1

    return count


def count_sentences(text):
    count = 0
    for i in range(len(text)):
        if text[i] == "." or text[i] == "!" or text[i] == "?":
            count += 1

    return count


def grade_level(letters, words, sentences):
    lets100 = letters / words * 100
    sens100 = sentences / words * 100
    index = 0.0588 * lets100 - 0.296 * sens100 - 15.8

    return round(index)


if __name__ == "__main__":
    main()