#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int gradeLevel(int letters, int words, int sentences);

int main(void)
{
    // get text with get_string
    string text = get_string("Text: ");

    // count letters (a-z, A-Z)
    int letters = count_letters(text);

    //count words (any sequence of characters separated by a space)
    int words = count_words(text);

    //count sentences (marked by . ! ?)
    int sentences = count_sentences(text);

    //print Grade X (X = grade level)
    int grade = gradeLevel(letters, words, sentences);

    if (grade < 1) //if grade is <1, print before grade 1
    {
        printf("Before Grade 1\n");
    }

    else if (grade > 16) //if grade is 16+, print grade 16+
    {
        printf("Grade 16+\n");
    }

    else // otherwise print the rounded grade level
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int length = strlen(text);
    int lets = 0; // for the number of letters

    for (int i = 0; i <= length; i++)
    {
        if (isalpha(text[i])) // if the char is a letter
        {
            lets++; // count 1 letter
        }
    }

    return lets;
}

int count_words(string text)
{
    int length = strlen(text);
    int wrds = 1; //starting at 1 because the last word of a string will not end in a space

    for (int i = 0; i <= length; i++)
    {
        if (isspace(text[i])) //if char is a space
        {
            wrds++;
        }
    }

    return wrds;
}

int count_sentences(string text)
{
    int length = strlen(text);
    int sents = 0; //for counting sentences

    for (int i = 0; i <= length; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sents++;
        }
    }

    return sents;
}

int gradeLevel(int letters, int words, int sentences)
{
    float lets100 = ((float)letters / (float)words * 100.0);
    float sens100 = ((float)sentences / (float)words * 100.0);
    float index = 0.0588 * lets100 - 0.296 * sens100 - 15.8;

    return round(index);
}
