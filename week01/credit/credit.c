#include <cs50.h>
#include <stdio.h>

// AMEX: 15 digit, starting with 34 or 37
// VISA: 13 or 16 digits, starting with 4
// MASTERCARD: 16 digits, starting with 51-55
// CHECKSUM: Multiply every other digit by 2, starting with second-to-last digit
// Add those digits together
// Add to that sum the sum of the remaining digits
// If the total's last digit is 0 - (the %10 is equal to 0) then it is valid

int main(void)
{
    // loop to get credit card #; accepts only positive values
    long long credit;

    do
    {
        credit = get_long_long("Number: ");
    }
    while (credit < 0);

    // count digits
    long long digitCounter(long long x); //refer to bottom for function
    int const digits = digitCounter(credit);

    // Return any 1-12, 14, and 17+ digit answers as invalid
    if (digits <= 12 || digits == 14 || digits >= 17)
    {
        printf("INVALID\n");
        return 0;
    }

    //perform luhn's algorithm
    long long findLuhnSum(long long credit, int digits); //finds the sum total of luhn's algorithm
    long int lSum = findLuhnSum(credit, digits);

    // check for the last digit ending in 0 with luhn's algorithm
    if (lSum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // check 13 digit numbers start with 4; return VISA
    if (digits == 13 && credit > 4000000000000)
    {
        printf("VISA\n");
        return 0;
    }

    // check 15 digit numbers start with 34 or 37; return AMEX
    if (digits == 15)
    {
        if (credit > 340000000000000 && credit < 350000000000000)
        {
            printf("AMEX\n");
            return 0;
        }
        if (credit > 370000000000000 && credit < 380000000000000)
        {
            printf("AMEX\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }

    //check 16-digit VISA and MASTERCARDS
    if (digits == 16)
    {
        if (credit > 4000000000000000 && credit < 5000000000000000) //VISA if it starts with 4
        {
            printf("VISA\n");
            return 0;
        }
        if (credit > 5100000000000000 && credit < 5600000000000000) // MASTERCARD if it starts with 51-55
        {
            printf("MASTERCARD\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }

    else
    {
        printf("INVALID\n");
        return 0;
    }

}

//CREATED FUNCTIONS:
//digitCounter function
long long digitCounter(long long x)
{
    long long i = x;
    int digit = 0; //to record number of digits

    while (i > 1)
    {
        i = i / 10;
        digit++;
    }
    return digit;
}

long long findLuhnSum(long long credit, int digits)
{
    long long creditDigits = credit;
    long long firstToLast;
    long long secondToLast;
    long int luhnOne = 0;
    long int luhnTwo = 0;
    long int luhnSum = 0;
    int doubled = 0;

    switch (digits)
    {
        case 17:
            firstToLast = ((creditDigits % 100000000000000000) - (creditDigits % 10000000000000000)) / 10000000000000000;
            luhnTwo = luhnTwo + firstToLast;

        case 16:
            secondToLast = (((creditDigits % 10000000000000000) - (creditDigits % 1000000000000000)) / 1000000000000000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }
            luhnOne = luhnOne + secondToLast;

        case 15:
            firstToLast = ((creditDigits % 1000000000000000) - (creditDigits % 100000000000000)) / 100000000000000;
            luhnTwo = luhnTwo + firstToLast;


        case 14:
            secondToLast = (((creditDigits % 100000000000000) - (creditDigits % 10000000000000)) / 10000000000000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 13:
            firstToLast = ((creditDigits % 10000000000000) - (creditDigits % 1000000000000)) / 1000000000000;
            luhnTwo = luhnTwo + firstToLast;


        case 12:
            secondToLast = (((creditDigits % 1000000000000) - (creditDigits % 100000000000)) / 100000000000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 11:
            firstToLast = ((creditDigits % 100000000000) - (creditDigits % 10000000000)) / 10000000000;
            luhnTwo = luhnTwo + firstToLast;


        case 10:
            secondToLast = (((creditDigits % 10000000000) - (creditDigits % 1000000000)) / 1000000000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;

        case 9:
            firstToLast = ((creditDigits % 1000000000) - (creditDigits % 100000000)) / 100000000;
            luhnTwo = luhnTwo + firstToLast;


        case 8:
            secondToLast = (((creditDigits % 100000000) - (creditDigits % 10000000)) / 10000000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 7:
            firstToLast = ((creditDigits % 10000000) - (creditDigits % 1000000)) / 1000000;
            luhnTwo = luhnTwo + firstToLast;


        case 6:
            secondToLast = (((creditDigits % 1000000) - (creditDigits % 100000)) / 100000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 5:
            firstToLast = ((creditDigits % 100000) - (creditDigits % 10000)) / 10000;
            luhnTwo = luhnTwo + firstToLast;


        case 4:
            secondToLast = (((creditDigits % 10000) - (creditDigits % 1000)) / 1000);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 3:
            firstToLast = ((creditDigits % 1000) - (creditDigits % 100)) / 100;
            luhnTwo = luhnTwo + firstToLast;


        case 2:
            secondToLast = (((creditDigits % 100) - (creditDigits % 10)) / 10);

            doubled = (secondToLast * 2);
            if (doubled > 9)
            {
                secondToLast = (((doubled - (doubled % 10)) / 10) + (doubled % 10));
            }
            else
            {
                secondToLast = (secondToLast * 2);
            }

            luhnOne = luhnOne + secondToLast;


        case 1:
            firstToLast = creditDigits % 10;
            luhnTwo = luhnTwo + firstToLast;

    }
    luhnSum = luhnOne + luhnTwo;
    return luhnSum;
}