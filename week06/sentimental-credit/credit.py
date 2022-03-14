from cs50 import get_int


def main():
    # Get credit card number from user
    while True:
        credit = get_int("Number: ")
        if credit > 0:
            break

    # Get length
    digits = len(str(credit))

    # Return any too-long or too-short numbers as invalid
    if digits <= 12 or digits == 14 or digits >= 17:
        print("INVALID")
        return 0

    # Perform Luhn's Algorithm
    if Luhns_Algorithm(credit) == False:
        print("INVALID")
        return 0

    # VISA if it's 13 digits and begins with 4
    if digits == 13 and str(credit)[0] == "4":
        print("VISA")
        return 0

    # AMEX if it's 15 digits and starts with 34 or 37
    if digits == 15:
        if str(credit)[0:2] == "34":  # if first digits are 34
            print("AMEX")
            return 0
        if str(credit)[0:2] == "37":  # if first digits are 37
            print("AMEX")
            return 0
        else:
            print("INVALID")
            return 0

    # VISA / MASTERCARD check for 16 digit numbers
    if digits == 16:
        if str(credit)[0] == "4":  # if first digit is 4
            print("VISA")
            return 0
        if int(str(credit)[0:2]) >= 51 and int(str(credit)[0:2]) <= 55:
            print("MASTERCARD")
            return 0
        else:
            print("INVALID")
            return 0

    # If none of the above cases apply, the card must be invalid.
    else:
        print("INVALID")
        return 0


# Performs Luhn's Algorithm in full
def Luhns_Algorithm(credit_number):
    step1 = Luhn_Step1(credit_number)
    step2 = Luhn_Step2(credit_number)
    answer = step1 + step2

    if answer % 10 == 0:
        return True
    else:
        return False


def Luhn_Step1(credit_number):
    num = int(credit_number / 10)
    product = 0

    while True:
        dig = num % 10
        doubled = dig * 2
        if doubled > 9:
            product += ((doubled - doubled % 10) / 10) + (doubled % 10)
        else:
            product += doubled
        num = int(num / 100)
        if num == 0:
            break

    return product


def Luhn_Step2(credit_number):
    num = credit_number
    answer = 0
    while True:
        answer += num % 10
        num = int(num / 100)
        if num == 0:
            break

    return answer


if __name__ == "__main__":
    main()