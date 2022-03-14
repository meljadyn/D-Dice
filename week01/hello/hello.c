#include <stdio.h>
#include <cs50.h> // required for get_string

int main(void)
{
    string name = get_string("What is your name? "); // gets name
    printf("hello, %s\n", name); // prints "hello, [name]"
}