#!/usr/bin/env python
"""A no-frills implementation of a timelock algorithm."""
import binascii
import md5

__author__ = "Cyrus Struble"
__email__ = "QuestionableRobot@gmail.com"


def timelock(epoch_time):
    """
    Take an epoch time and produce the timelock value for it.

    Calculates the timelock value by (ideally) taking the first
    two letters of the hash along with the last two numbers of
    the hash in reverse order.

    Returns a tuple with (hash, timelock_value).
    """
    # double-pass md5 hash
    first_pass = binascii.b2a_hex(md5.new(str(epoch_time)).digest())
    md5_hash = binascii.b2a_hex(md5.new(first_pass).digest())

    result = ""
    num_letters = sum(c.isalpha() for c in md5_hash)
    num_digits = sum(n.isdigit() for n in md5_hash)
    # zero or one letter in hash
    if (num_letters < 2):
        result = less_than_two_letter_hash_to_timelock(md5_hash)

    # zero or one single-digit integer in hash
    elif (num_digits < 2):
        result = less_than_two_digit_hash_to_timelock(md5_hash)

    # normal case
    else:
        result = normal_hash_to_timelock(md5_hash)

    return ((md5_hash, result))


def normal_hash_to_timelock(md5_hash):
    """
    Take a typical md5 hash and return its timelock value.

    A typical md5 hash is one with at least two alphabetic chracters
    and two numbers. The resulting timelock value is the first two
    characters of the hash and the last two numbers of the hash
    reversed.
    """
    result = ""
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

    return (result)


def less_than_two_digit_hash_to_timelock(md5_hash):
    """
    Take a md5 hash with less than two digits and return its timelock value.

    The resulting timelock value is two letters, followed by up to one number
    from the end of the hash, and filled in with remaining letters.
    """
    result = ""
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

    return (result)


def less_than_two_letter_hash_to_timelock(md5_hash):
    """
    Take a md5 hash with less than two letters and return its timelock value.

    The resulting timelock value is up to two letters, filled in with
    remaining numbers from the end of the hash, in reverse order.
    """
    result = ""
    num_appends = 0
    for c in md5_hash:
        if (c.isalpha()):
            result += c
            num_appends += 1

    for n in reversed(md5_hash):
        if (n.isdigit() and num_appends < 4):
            result += n
            num_appends += 1

    return (result)


if __name__ == '__main__':
    epoch_time = 421141380
    print(timelock(epoch_time)[1])
