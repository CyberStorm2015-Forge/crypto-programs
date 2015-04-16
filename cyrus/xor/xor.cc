/****************************************************
 * <Cyrus Struble>
 * <4/16/2015>
 * <xor.cc>
 *
 * <A simple command-line application that processes
 *  a data file with a file named key in the current
 *  directory, XOR'ing the two and printing the result
 *  to stdout.>
 ****************************************************/
#include <vector>
#include <fstream>
#include <iostream>
#include <bitset>
#include <stdio.h>
using namespace std;

// function prototypes
void Process(char const*, char const*);
static vector<char> ReadAllBytes(char const*);

int main(int argc, char** argv)
{
    char const* keyfile = "key";
    char const* cipherfile;

    if (argc < 2)
    {
        printf("usage: %s FILENAME\n\npositional arguments:\n\tFILENAME\t\tthe file to XOR with the key file in the current directory\n\n", argv[0]);
        exit(0);
    } else {
        // ./xor < ciphertext >
        cipherfile = argv[1];
        printf("Cipher filename: %s\n", cipherfile);
        Process(cipherfile, keyfile);
    }
    return 0;
}

/* Processes a given data file with a given keyfile,
   XOR'ing the binary data of each and printing the result
   to stdout.*/
void Process(char const* datafile, char const* keyfile)
{
    // read the data for file and key in as a vector of bytes
    vector<char> filebytes = ReadAllBytes(datafile);
    printf("Number of file bytes: %lu\n", filebytes.size());

    vector<char> keybytes = ReadAllBytes(keyfile);
    printf("Number of key bytes: %lu\n", keybytes.size());

    // if the file and key don't have the same number of bytes, quit
    if (filebytes.size() != keybytes.size())
    {
        printf("File (%lu bytes) and Key (%lu bytes) aren't same size\n", filebytes.size(), keybytes.size());
        exit(1);
    }

    // convert to a vector of bitsets for easier processing
    vector< bitset<8> > filebits;
    for (char c : filebytes)
        filebits.push_back(bitset<8>(c));

    vector< bitset<8> > keybits;
    for (char c : keybytes)
        keybits.push_back(bitset<8>(c));

    vector < bitset<8> > plaintextbits;
    // XOR operation, storing the results as bitsets in plaintextbits
    int i = 0;
    while (i < filebits.size())
    {
        plaintextbits.push_back(filebits[i]^keybits[i]);
        i++;
    }

    // Print message to stdout
    for (bitset<8> b : plaintextbits)
        cout << static_cast<char>(b.to_ulong());
    cout << endl;
}

/* Takes a filename and returns a vector of chars
   representing the bytes of that file. */
static vector<char> ReadAllBytes(char const* file)
{
    ifstream ifs(file, ios::binary|ios::ate);
    ifstream::pos_type pos = ifs.tellg();

    vector<char>  result(pos);

    ifs.seekg(0, ios::beg);
    ifs.read(&result[0], pos);

    return result;
}
