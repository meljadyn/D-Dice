#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Const for block size
    const int BLOCK_SIZE = 512;

    // Check command-line arguments
    if (argc != 2)
    {
        printf("Invalid call.\nUsage: ./recover MEMORY_CARD_FILE\n");
        return 1;
    }

    // Check that file opens
    FILE *cardData = fopen(argv[1], "r");
    if (cardData == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Set naming convention
    char *jpgName = malloc(8); // make space for jpgName in sprintf
    int i = 0; // jpeg number
    sprintf(jpgName, "%03i.jpg", i); // naming convention

    // open a fresh jpg to write to
    FILE *image = fopen(jpgName, "a");
    if (image == NULL)
    {
        printf("FILE *image did not open on first call.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE]; // to store read data
    bool open = false; // checks if a file is being written to

    // iterate over each block in the card
    while (fread(buffer, 1, BLOCK_SIZE, cardData) == BLOCK_SIZE)
    {
        // if jpeg header is found (0xff, 0xd8, 0xff, 0xe0-oxef)
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if ((buffer[3] & 0xf0) == 0xe0) // resets last four bits to 0
            {
                if (open == false) // if this is the first jpeg
                {
                    fwrite(&buffer, 1, BLOCK_SIZE, image);
                    open = true; // set open to true to indicate a writing file is active
                }

                else  // if this is the start of a new jpeg
                {
                    fclose(image); // close old file
                    i++; // increment jpeg name
                    sprintf(jpgName, "%03i.jpg", i); // naming convention
                    image = fopen(jpgName, "a"); // make new file to write into
                    if (image == NULL)
                    {
                        printf("FILE *image did not open upon new jpeg signature\n");
                        return 1;
                    }
                    fwrite(&buffer, 1, BLOCK_SIZE, image); // write into new jpeg
                }
            }
        }
        else // else, if there is no jpeg header
        {
            if (open == true) // if we have found at least one jpeg so far
            {
                fwrite(&buffer, 1, BLOCK_SIZE, image); // append buffer into active file
            }
        }
    }

    // Close files and free mallocs
    fclose(cardData);
    fclose(image);
    free(jpgName);
}