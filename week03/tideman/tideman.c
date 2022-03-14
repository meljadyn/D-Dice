#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0) // if a candidate matches the name
        {
            ranks[rank] = i; // record their rank position
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // this function is called once per voter, and records preferences;
    // add one to preferences[i][j] where candidate i is preferred over candidate j

    for (int i = 0; i < (candidate_count - 1); i++)
    {
        for (int j = i + 1; j < candidate_count; j++) // counts ever candidate behind i in rank
        {
            preferences[ranks[i]][ranks[j]]++; // records those candidates
        }
    }

    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int k = 0; // pair number
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (i != j)
            {
                if (preferences[i][j] > preferences[j][i]) // records the winner i
                {
                    pairs[k].winner = i;
                    pairs[k].loser = j;
                    k++;
                }
            }
        }
    }

    pair_count = k;

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // sort the pairs in decreasing order from strength of victory (most preferred to least preferred)
    // order doesn't matter if multiple pairs has the same strength of victory

    int pairStrength[pair_count]; //an array to record the strength of each pair

    for (int i = 0; i < pair_count; i++)
    {
        // records pair strength in new array
        pairStrength[i] = preferences[pairs[i].winner][pairs[i].loser];
    }

    int highest = -1; // to store highest scoring candidate

    for (int i = 0; i < pair_count; i++)
    {
        int score = 0;

        // searches for highest scoring candidate so it can be sorted into i position
        for (int j = i; j < pair_count; j++)
        {
            if (pairStrength[j] > score)
            {
                score = pairStrength[j];
                highest = j;
            }
        }

        // temporarily store the pair/strength value of i
        int temp1 = pairStrength[i];
        pair temp2 = pairs[i];

        // move the pair/strength value of highest candidate into i
        pairStrength[i] = pairStrength[highest];
        pairs[i] = pairs[highest];

        // put i's old value in the old highest's spot
        pairStrength[highest] = temp1;
        pairs[highest] = temp2;
    }

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // function returns false if a cycle is formed (true if there is still a valid source)
    bool sourceCheck(int currentPair, int winner, int loser);

    for (int i = 0; i < (pair_count); i++) // locks in all pairs
    {
        locked[pairs[i].winner][pairs[i].loser] = true;
        // test current pair to see if it will cause a cycle
        bool check = sourceCheck(i, pairs[i].winner, pairs[i].loser);
        if (check == false) // false means it caused a cycle
        {
            locked[pairs[i].winner][pairs[i].loser] = false; // if false, unlock the locked pair
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // print the source of the graph; you can assume there will only be one source

    for (int i = 0; i < candidate_count; i++)
    {
        int locks = 0;

        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == false)
            {
                locks++;
            }
        }

        if (locks == candidate_count)
        {
            printf("%s\n", candidates[i]);
        }
    }

    return;
}

// Returns true if there is a cycle
bool sourceCheck(int currentPair, int winner, int loser)
{
    for (int i = 0; i <= currentPair; i++)
    {
        int locks = 0; //false lock counter
        int counter = 0; //counts iterations regardless of true/false

        for (int j = 0; j <= currentPair; j++)
        {
            counter++;
            if (locked[pairs[i].loser][pairs[j].winner] == false)
            {
                locks++;
            }
        }
        // if at least one person has all false inputs going to them, they are still a source and there is not a cycle.
        if (locks == counter)
        {
            return true;
        }
    }

    return false;
}