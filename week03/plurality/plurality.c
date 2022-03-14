#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{

    for (int i = 0; i < candidate_count; i++) // loop up to the max number of candidates times
    {
        if (strcmp(candidates[i].name, name) == 0) //if the names match
        {
            candidates[i].votes++; //increment that candidate's vote
            return true;
        }
    }

    return false; // if candidate was not found
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    for (int i = 1; i < candidate_count; i++)
    {
        if (candidates[0].votes < candidates[i].votes) //puts the candidate with the highest vote at the array [0]
        {
            string tempName = candidates[0].name; //temporarily stores candidate0's info
            int tempVotes = candidates[0].votes;

            candidates[0].votes = candidates[i].votes; //replaces candidate0's info with i's
            candidates[0].name = candidates[i].name;
            candidates[i].name = tempName; //puts candidate0's info in i's old spot
            candidates[i].votes = tempVotes;
        }
    }

    printf("%s\n", candidates[0].name);

    // checks for ties in score and prints their name as well
    for (int i = 1; i < candidate_count; i++)
    {
        if (candidates[0].votes == candidates[i].votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }

    return;
}