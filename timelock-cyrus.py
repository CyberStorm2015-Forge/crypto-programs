#!/usr/bin/env python
"""
A no-frills implementation of a timelock algorithm.
"""
import md5
import binascii

__author__ = "Cyrus Struble"
__email__ = "QuestionableRobot@gmail.com"

def timelock(epoch_time):
    """
    Takes a given time in seconds since the epoch,
    processes the md5 hash of the md5 hash of it,
    and returns a timelock code consisting of the
    first two letters and last two numbers in reverse,
    as well as the hash.
    """
    # double-pass md5 hash
    md5_hash = binascii.b2a_hex(md5.new(binascii.b2a_hex(md5.new(str(epoch_time)).digest())).digest())

    result = ""
    num_letters = sum(c.isalpha() for c in md5_hash)
    num_digits = sum(n.isdigit() for n in md5_hash)
    # case 1: zero or one letter in hash
    if (num_letters < 2):
        num_appends = 0
        for c in md5_hash:
            if (c.isalpha()):
                result += c
                num_appends += 1

        for n in reversed(md5_hash):
            if (n.isdigit() and num_appends < 4):
                result += n
                num_appends += 1

    # case 2: zero or one single-digit integer in hash
    elif (num_digits < 2):
        num_appends = 0
        for c in md5_hash:
            if (c.isalpha() and num_appends < 2):
                result += c
                num_appends += 1
            elif (c.isdigit() and num_appends >= 2):
                result += c
                num_appends += 1
            elif (c.isalpha() and num_appends < 4):
                result += c
                num_appends += 1

    # case 3: normal case
    else:
        # append the first two alphabetic characters
        num_appends = 0
        for c in md5_hash:
            if (c.isalpha() and num_appends < 2):
                result += c
                num_appends += 1

        # append the last two numeric characters in reverse order
        num_appends = 0
        for n in reversed(md5_hash):
            if (n.isdigit() and num_appends < 2):
                result += n
                num_appends += 1

    return((md5_hash, result))

if __name__ == '__main__':
    epoch_time = 421141380 # 4/15/2015 20:30:00
    print(timelock(epoch_time)[1])
