#!/usr/bin/env python3
"""
    Runs Nussinov's Algorithm to find optimal substructure for RNA sequences
"""
# @Author: jmwolff3

import argparse
import numpy as np
from os import path


def setParser():
    """
    Argument Parser for the nussinov program
    
    Returns:
        parser: argument parser
    """
    parser = argparse.ArgumentParser(prog="Nussinov Algorithm Solver", description="A program that runs Nussinov's Algorithm on a given RNA strand and returns the most viable parings.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--filepath", help="the path to a text file with a sequence")
    group.add_argument("-s", "--sequence", help="the RNA sequence to evaluate")
    parser.add_argument("-v", "--verbose", action="store_true", help="More verbose output")
    return parser


def getSequence(args):
    """
    Takes passed arguments from script and loads the sequence from file or from input string
    
    Args:
        args (args): Function Arguments
    
    Returns:
        sequence (string): sequence string or None
    """
    sequence = args.sequence

    if sequence in [None, "", ''] and args.filepath not in [None, "", '']:
        if path.exists(args.filepath):
            try:
                with open(args.filepath, "r+") as file:
                    sequence = file.readline()
            except Exception as e:
                print("An excepttion occured.", e)
                return None
    return sequence

def isSequenceValid(sequence):
    """
    Validates the sequence contains only valid strings
    
    Args:
        sequence (string): sequence string
    
    Returns:
        boolean: True if only allowed characters, False if None or uses other characters
    """
    if not sequence:
        return False
    allowed_chars = set('GCAU')
    return set(sequence).issubset(allowed_chars)


def cost_function(a, b):
    """
    Determines the cost associated with a pair, 1 if in valid pairs, else 0
    This function gives 1 cost to UG pairs as well

    Args:
        a (character): first character in pair
        b (character): second character in pair

    Returns:
        int: 1 if in valid pairs else 0
    """
    pairs = [('G', 'C'), ('C', 'G'), ('A', 'U'), ('U', 'A'), ('G', 'U'), ('U', 'G')]
    
    if (a, b) in pairs:
        return 1
    return 0

def classicalNussinov(sequence):
    """
    Nussinov's Algorithm

    Args:
        sequence (string): the sequence to run the algorithm on

    Returns:
        M (Matrix): a nxn matrix contianing the scores for each index
    """
    len_seq = len(sequence)
    M = np.zeros((len_seq, len_seq))

    for d in range(1, len_seq):
        for i in range(len_seq-d):
            j = i+d
            temp = M[i+1][j-1] + cost_function(sequence[i], sequence[j])
            for k in range(i, j):
                temp = max(temp, M[i][k]+M[k+1][j])
            M[i][j] = temp
    return M

def backtrace(sequence, M, P, i, j):
    """
    The backtrace that generates the optimal structure

    Args:
        sequence (string): The sequence string
        M (Matrix): the scoring matrix
        P (Array): an array of pairs of indices
        i (int): starting value
        j (int): ending value

    Returns:
        None
    """
    if j <= i:
        return

    if M[i][j] == M[i][j-1]:
        backtrace(sequence, M, P, i, j-1)
    
    else:
        for k in range(i, j):
            if cost_function(sequence[k], sequence[j]):
                if k-1 < 0:
                    if M[i][j] == M[k+1][j-1]+1:
                        if (k,j) not in P:
                            P.append((k,j))
                        backtrace(sequence, M, P, k+1, j-1)
                if M[i][j] == M[i, k-1] + M[k+1][j-1] + 1:
                    if (k,j) not in P:
                        P.append((k,j))
                    backtrace(sequence, M, P, i, k-1)
                    backtrace(sequence, M, P, k+1, j-1)
                    break;

def structure_output(sequence, P):
    """
    Function to create the structure string from the matrices

    Args:
        sequence (string): The sequence string
        P (array): The array of indices

    Returns:
        (string): The string of the substruture in dot bracket notation
    """
    structure = ["." for _ in range(len(sequence))]
    for pair in P:
        structure[pair[0]] = "("
        structure[pair[1]] = ")"
    return "".join(structure)

def main():
    parser = setParser()
    args = parser.parse_args()
    verbose = args.verbose


    sequence = getSequence(args)
    if not isSequenceValid(sequence):
        print("Your sequence is invalid.")
        return -1

    M = classicalNussinov(sequence)
    pairs = []
    backtrace(sequence, M, pairs, 0, len(sequence)-1)

    print(sequence)
    print(structure_output(sequence, pairs))

    if verbose:
        print(M)

    return

if __name__ == '__main__':
    main()