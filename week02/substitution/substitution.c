#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

string cipherConvert(string text, string key);

int main(int argc, string argv[])
{
    //Key must contain 26 characters.

    if (argc != 2) // rejects call if there are no or too many arguments
    {
        printf("Must include key when calling program.\n");
        return 1;
    }

    string key = argv[1]; //turns command argument into a string
    if (strlen(key) != 26) //rejects you if you don't have 26 letters
    {
        printf("Key must be exactly 26 letters.\n");
        return 1;
    }

    for (int i = 0; i < 26; i++) //checking for only letters
    {
        if (isalpha(key[i]))
        {
            i++;
        }
        else
        {
            printf("Key must use only letters.");
            return 1;
        }
    }

    for (int i = 0; i < 26; i++) //checks for duplicate characters
    {
        for (int j = i + 1; j < (26 - i); j++)
        {
            if (key[i] == key[j])
            {
                printf("Key must have no duplicate letters.\n");
                return 1;
            }
        }
    }

    string text = get_string("plaintext: ");
    string cipherText = cipherConvert(text, key);

    printf("ciphertext: %s", cipherText);
    printf("\n");
}

string cipherConvert(string text, string key)
{
    int length = strlen(text);
    string cipher = text;

    for (int i = 0; i < length; i++)
    {
        if isupper(text[i])
        {
            cipher[i] = toupper(key[text[i] - 65]);
        }
        else if islower(text[i])
        {

            cipher[i] = tolower(key[text[i] - 97]);
        }
        else // if it is not a letter
        {
            cipher[i] = text[i];
        }
    }

    return cipher;
}

//ABCDEFGHIJKLMNOPQRSTUVWXYZ
//VCHPRZGJNTLSKFBDQWAXEUYMOI
//HELLO
