#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

char *get_filtered_input(FILE *fd, char *mask);

int main(int argc, char *argv[])
{
	if(argc < 2 || (strcmp(argv[1],"-d") && strcmp(argv[1],"-e")))  
	{
		printf("Usage: %s (-e,-d) <bit_length>\n",argv[0]);
		return 0;
	}

	char *input;
	if(strcmp(argv[1], "-d") == 0)
		input = get_filtered_input(stdin, "01");
	else
		input = get_filtered_input(stdin, NULL);
	printf(" \n");

	if(input != NULL)
	{
		int len;
		int bit_length;
		char *final = NULL;
		if(strcmp(argv[1], "-d") == 0)
		{
			if(strlen(input) %8 == 0)
				bit_length = 8;
			else if(strlen(input) %7 == 0)
				bit_length = 7;
			else
			{
				printf("error: Input string length (%d) is not divisible by 7 or 8\n",strlen(input));
				return 0;
			}

			len = strlen(input)/bit_length;
			final = calloc(len+1, sizeof(char));

			int i;
			for(i = 0; i < len; i++)
			{
				int j;
				for(j = 0; j < bit_length; j++)
				{
					if(input[i*bit_length+bit_length-j-1] == '1') //byte*bits_per_byte+bits_per_byte-offset-1
						final[i] |= (0x01 << j);
				}
			}
			final[len] = '\0';

			printf("%s\n",final);
		}
		else if(strcmp(argv[1],"-e") == 0)
		{
			if(argc < 3 || (strcmp(argv[2],"7") && strcmp(argv[2],"8")))  
				bit_length = 8;
			else
				bit_length = atoi(argv[2]);

			len = strlen(input)*bit_length;
			final = calloc(len+1, sizeof(char));

			int i;
			for(i = 0; i < strlen(input); i++)
			{
				int j;
				for(j = 0; j < bit_length; j++)
				{
					if((input[i] & (0x01 << bit_length-j-1))) //byte*bits_per_byte+bits_per_byte-offset-1
						final[i*bit_length+j] = '1';
					else
						final[i*bit_length+j] = '0';
				}
			}
			final[len] = '\0';
			printf("%s\n",final);
		}
	}
	else
	{
		printf("error: No input matched mask\n");
	}
	return 0;
}

/* Purpose: Filter input from file and return filtered characters in a cstring 
 * Input: File Descriptor pointer and null terminated  cstring contain allowed characters
 * Output: Null Terminated cstring or NULL if no input matched mask
 * NOTE: Does not handle opening or closing of file
 * Written: 10/22/12
*/
char *get_filtered_input(FILE *fd, char *mask)
{
	char character;
	int size = 0;
	char * sequence = NULL;
	while((character = fgetc(fd)) != EOF) //probably really wastful overhead wise reallocing EVERYTIME!
	{
		int i;
		for(i = 0; i < (mask != NULL)?strlen(mask):1; i++)
		{
			if(character == (mask != NULL)?mask[i]:character)
			{
				sequence = realloc(sequence, ++size+1);
				sequence[size-1] = character; //Last byte is for null terminator
				break;
			}
		}
	}
	if(sequence != NULL)
		sequence[size] = '\0'; //Null Terminator
	return sequence;
}
