/*******************************************
Program Description: encodes ascii to binary
Author: Jack Mertens
Date: 4/15/15
*******************************************/

#include <stdio.h>
#include <iostream>
#include <bitset>
#include <string>
#include <stdlib.h> 

//adjust the base size as necessary
#define base 7

using namespace std;

int main()
{
	string input;
	string output;
	
	int index = 0;
	
	//wait for input
	while(cin)
	{
		cout << "decoder % ";
		getline(cin,input);

		for(int i=0; i<input.length(); i+=base)
		{
			//cout << "Going through the motions" << endl;
			bitset<base> bit(input.substr(i,base));
			char c = char(bit.to_ulong());
			//cout << c << endl;
			output+= c;
		}
		cout << output << endl;
	}
	
	return 0;
}
