#include "helpers.h"
#include <math.h>

void average(int height, int width, int row, int column, RGBTRIPLE copy[height][width]);
void gMatrix(int height, int width, int row, int column, RGBTRIPLE copy[height][width]);

// global variables to be updataed by average function
int averageRed = 0;
int averageGreen = 0;
int averageBlue = 0;

// global variables to be updated by matrix function
int redGx = 0;
int greenGx = 0;
int blueGx = 0;

int redGy = 0;
int greenGy = 0;
int blueGy = 0;

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // takes average brightness of pixels
            float average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;

            int avg = round(average);

            // copies average value into each pixel
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width]; // for copying pixel data
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // save left pixel into temp variable
            temp[i][j] = image[i][j];

            // copy matching right pixel into left pixel
            image[i][j] = image[i][width - (j + 1)];

            // copy left pixel into right pixel
            image[i][width - (j + 1)] = temp[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    // Create a copy of image
    for (int i = 0; i <= height - 1; i++)
    {
        for (int j = 0; j <= width - 1; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // blurring for all pixels
    for (int i = 0; i <= height - 1; i++)
    {
        for (int j = 0; j <= width - 1; j++)
        {
            average(height, width, i, j, copy); // call to update global avg functions

            // update pixel rgb values with the averages
            image[i][j].rgbtRed = averageRed;
            image[i][j].rgbtBlue = averageBlue;
            image[i][j].rgbtGreen = averageGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    // Create a copy of image
    for (int i = 0; i <= height - 1; i++)
    {
        for (int j = 0; j <= width - 1; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Replace values with valye from gx/gy matrixes
    for (int i = 0; i <= height - 1; i++)
    {
        for (int j = 0; j <= width - 1; j++)
        {
            // call to update global matrix functions
            gMatrix(height, width, i, j, copy);

            // perform sqrt formula on the global matrix functions
            double red = sqrt((redGx * redGx) + (redGy * redGy));
            double green = sqrt((greenGx * greenGx) + (greenGy * greenGy));
            double blue = sqrt((blueGx * blueGx) + (blueGy * blueGy));

            // cap at 255
            if (red > 255)
            {
                red = 255;
            }

            if (green > 255)
            {
                green = 255;
            }

            if (blue > 255)
            {
                blue = 255;
            }

            // update pixel rgb values with the g matrix results
            image[i][j].rgbtRed = round(red);
            image[i][j].rgbtBlue = round(blue);
            image[i][j].rgbtGreen = round(green);
        }
    }
    return;
}

// finds the average of every color in a 3 x 3 grid and updates the avg global variables accordingly
void average(int height, int width, int row, int column, RGBTRIPLE copy[height][width])
{
    // create local color variables
    float n = 0;
    float red = 0;
    float green = 0;
    float blue = 0;

    for (int i = (row - 1); i <= (row + 1); i++)
    {
        for (int j = (column - 1); j <= (column + 1); j++)
        {
            // makes sure that it only counts valid pixels (not going over edges/corners)
            if (i >= 0 && i <= (height - 1) && j >= 0 && (j <= width - 1))
            {
                n++; //keeps count of valid pixels
                red += copy[i][j].rgbtRed;
                green += copy[i][j].rgbtGreen;
                blue += copy[i][j].rgbtBlue;

            }
        }
    }

    // update global variables with pixel specific information
    averageRed = round(red / n);
    averageGreen = round(green / n);
    averageBlue = round(blue / n);
}

void gMatrix(int height, int width, int row, int column, RGBTRIPLE copy[height][width])
{
    // reset global variables
    redGx = 0;
    greenGx = 0;
    blueGx = 0;

    redGy = 0;
    greenGy = 0;
    blueGy = 0;

    void GxFormula(int height, int width, int n, int row, int column, RGBTRIPLE copy[height][width]);
    void GyFormula(int height, int width, int n, int row, int column, RGBTRIPLE copy[height][width]);

    // top left
    if (row > 0 && column > 0)
    {
        GxFormula(height, width, -1, row - 1, column - 1, copy);
        GyFormula(height, width, -1, row - 1, column - 1, copy);
    }

    // top middle
    if (row > 0)
    {
        GyFormula(height, width, -2, row - 1, column, copy);
    }

    // top right
    if (row > 0 && column < width - 1)
    {
        GxFormula(height, width, 1, row - 1, column + 1, copy);
        GyFormula(height, width, -1, row - 1, column + 1, copy);
    }

    // middle left
    if (column > 0)
    {
        GxFormula(height, width, -2, row, column - 1, copy);
    }

    // middle right
    if (column < width - 1)
    {
        GxFormula(height, width, 2, row, column + 1, copy);
    }

    // bottom left
    if (row < height - 1 && column > 0)
    {
        GxFormula(height, width, -1, row + 1, column - 1, copy);
        GyFormula(height, width, 1, row + 1, column - 1, copy);
    }

    // bottom middle
    if (row < height - 1)
    {
        GyFormula(height, width, 2, row + 1, column, copy);
    }

    // bottom right
    if (row < height - 1 && column < width - 1)
    {
        GxFormula(height, width, 1, row + 1, column + 1, copy);
        GyFormula(height, width, 1, row + 1, column + 1, copy);
    }
}

void GxFormula(int height, int width, int n, int row, int column, RGBTRIPLE copy[height][width])
{
    redGx += (n * copy[row][column].rgbtRed);
    greenGx += (n * copy[row][column].rgbtGreen);
    blueGx += (n * copy[row][column].rgbtBlue);
}

void GyFormula(int height, int width, int n, int row, int column, RGBTRIPLE copy[height][width])
{
    redGy += (n * copy[row][column].rgbtRed);
    greenGy += (n * copy[row][column].rgbtGreen);
    blueGy += (n * copy[row][column].rgbtBlue);
}