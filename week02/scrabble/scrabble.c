#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }

    else // if score1 = score 2
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // Compute and return score for string
    int wordlen = strlen(word);
    int scoreArray[wordlen];
    int score = 0;

    for (int i = 0; i < wordlen; i++)
    {
        if (toupper(word[i]) >= 'A' && toupper(word[i]) <= 'Z')
        {
            //list score for word[i] in scoreArray[i] by referencing points[i]
            scoreArray[i] = POINTS[toupper(word[i]) - 65];
        }
        else
        {
            scoreArray[i] = 0;
        }
    }

    for (int i = 0; i < wordlen; i++)
    {
        score = score + scoreArray[i];  // add the score per letter to total score
    }
    return score;
}
