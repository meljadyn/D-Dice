// IMPORTANT NOTE: I was struggling with this lab and watched the provided video in the "not sure how to solve" section. That video explained the solution in full and I was able to understand and utilize that solution. For academic honesty reasons I wanted to disclose that this is not my solution; it's the solution from the video, which I implemented after I understood it. If that is a problem I can try to find an alternative solution.

// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Read the header from the input file - 44 bytes
    uint8_t header[HEADER_SIZE];
    fread(header, HEADER_SIZE, 1, input);

    // Write the header to the output file - 44 bytes
    fwrite(header, HEADER_SIZE, 1, output);

    // Read the sample from the input file
    int16_t buffer;
    int i = 0;

    //Note to self: fread returns 0 at end of file, which the while loop will treat as false
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        // Update volume
        buffer *= factor;

        // Write the new files to output
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}