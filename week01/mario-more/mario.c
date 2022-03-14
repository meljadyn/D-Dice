#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: "); //user picks height
    }
    while (height < 1 || height > 8);

    int row = 1; //establishes current row
    for (int j = 0; j < height; j++)
    {
        for (int i = 0; i < (height - row); i++) //print " " (height minus row) times e.g. " " (8-1) aka 7 times
        {
            printf(" ");
        }
        for (int i = row; i > 0; i--) //print "#" 1 rowNumber times
        {
            printf("#");
        }
        printf("  "); //print "  "
        for (int i = (row); i > 0; i--) //print "#" rowNumber times
        {
            printf("#");
        }
        printf("\n"); //start the next line
        row += 1; // add +1 to row counter
    }
}