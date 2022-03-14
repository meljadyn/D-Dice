// Implements a dictionary's functionality

#include <strings.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 9482;

// Hash table
node *table[N];

// Keeps count of words entered into dictionary
int numWords = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word); // Obtain hash value of word

    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next; // move the cursor down the list
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // represents the frequency of each first letter in a dictionary (the higher the number, the more frequent it is) --- USED WIKIPEDIA's "LETTER FREQUENCY" page for this information
    int firstFreq[27] = {0, 470, 680, 710, 610, 390, 410, 330, 720, 390, 110, 250, 310, 560, 220, 250, 770, 96, 600, 410, 500, 290, 70, 270, 5, 36, 24};

    int range[3];
    range[0] = 0; // lower bound
    range[1] = 0; // upper bound
    int j = 1;

    int length = strlen(word);

    // to find lower bound according to first letter
    for (int i = toupper(word[0]) - 65; i >= 0; i--)
    {
        while (i < 0 || i > 26)
        {
            i = toupper(word[j]) - 65;
            j++;
        }

        range[0] += firstFreq[i];
    }

    j = 1;
    // to find upper bound according to first letter
    for (int i = toupper(word[0]) - 64; i >= 0; i--)
    {
        while (i < 0 || i > 27)
        {
            i = (toupper(word[j]) - 65);
            j++;
        }
        range[1] += firstFreq[i];
    }

    // difference of upper and lower bound
    range[2] = range[1] - range[0];

    // takes the sum of all the ascii characters
    int sum = 0;
    for (int i = 0; i < length; i++)
    {
        sum += toupper(word[i]);
    }

    while (sum > range[2])
    {
        sum = sum / 10;
    }

    return range[0] + sum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open File
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Dictionary file could not be accessed.\n");
        return false;
    }

    // Create space to store the dictionary word
    char *dictWord = malloc(LENGTH + 1);
    if (dictWord == NULL)
    {
        printf("Not enough memory to make variable dictWord.\n");
        return false;
    }

    // Scan each word into the hash table
    while (fscanf(dict, "%s", dictWord) != EOF)
    {
        // Create a new node for storing the list
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Not enough memory to make new node.\n");
            return false;
        }

        int index = hash(dictWord); // get index for current word
        strcpy(n->word, dictWord);
        if (index < 0 || index > N - 1) // last check to ensure valid input
        {
            index = 4521;
        }
        n->next = table[index]; // point n at the same place as table's pointer
        table[index] = n; // point table at n
        numWords++; // keep track of words loaded from dictionary
    }

    // Close files and free the malloc'd memory that is no longer needed
    free(dictWord);
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (numWords == 0)
    {
        return 0;
    }
    else
    {
        return numWords;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
