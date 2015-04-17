#!/usr/bin/env python
"""
A command-line program to encrypt and decrypt ascii using
the Vigenere cipher.
"""

import argparse
import string

__author__ = "Cyrus Struble"
__email__ = "QuestionableRobot@gmail.com"


def vigenere(data, key, mode):
    """
    Encrypt some data with a vigenere cipher.

    Keyword arguments:
    data -- the ascii data to be encrypted/decrypted
    key -- the ascii key to encrypt/decrypt the given data
    mode -- whether to encrypt (1) or decrypt (-1) the data
    """
    result = ""
    num_nonchar = 0  # keep track of the number of non-alphabet characters
    stripped_key = key.replace(" ", "")  # remove key whitespace

    if (mode not in {1, -1}):
        print("Invalid mode. Use 1 for encryption or -1 for decryption.")
        quit()

    for c in range(0, len(data)):
            if (not data[c].isalpha()):  # if the data isn't alphabetic
                    result += data[c]
                    num_nonchar += 1
            elif (data[c].islower()):
                    index_of_char = string.lowercase.index(data[c])
                    key_alpha = stripped_key[(c - num_nonchar) % len(stripped_key)]
                    index_of_key = string.lowercase.index(key_alpha.lower())
                    result += string.lowercase[(index_of_char + (mode * index_of_key)) % 26]
            elif (data[c].isupper()):
                    index_of_char = string.uppercase.index(data[c])
                    key_alpha = stripped_key[(c - num_nonchar) % len(stripped_key)]
                    index_of_key = string.uppercase.index(key_alpha.upper())
                    result += string.uppercase[(index_of_char + (mode * index_of_key)) % 26]

    return(result)


if __name__ == '__main__':
        choices = {"encrypt": 1, "decrypt": -1}
        parser = argparse.ArgumentParser(description="encrypt/decrypt vigenere \
                                                        messages")
        parser.add_argument('role', choices=choices, help="whether to encrypt or\
                                                        decrypt")
        parser.add_argument('key', metavar='KEY', type=str, help="the ciper key \
                                                        to encode/decode with")
        args = parser.parse_args()
        mode = choices[args.role]
        key = args.key

        while True:
                data = raw_input("Message: ")
                output = vigenere(data, key, mode)
                print("Encrypted: {0}".format(output))
