# coding: UTF-8
"""
CONLL FORMAT CORPUS SPLITTER
"""
import random
import numpy as np


# def verbose(function):
#     """
#     Verbosity function with decorators
#     """
#     def wrapper(*args, **kwargs):
#         """
#         Verbosity wrapper
#         """
#         print("********** {} **********".format(function.__name__))
#         result = function(*args, **kwargs)
#         print("********** {} **********".format(function.__name__))
#         return result
#     return wrapper


# @verbose
def read_conll(filename, verbose=0):
    """
    types: (str) -> list
    structure: ("file name") -> list[list[str]]
    reads a conll text file and returns a list of lists of
    conll formatted lines.
    """
    if verbose > 0:
        print("Loading {}...".format(filename))
    conll_corpus = []
    a_conll_line = []
    for line in open(filename, 'r'):
        if not line.strip():
            if a_conll_line:
                conll_corpus.append(a_conll_line)
            a_conll_line = []
        else:
            if line[0] == "#":
                continue
            a_conll_line.append(line.split('\t'))
    if a_conll_line:
        conll_corpus.append(a_conll_line)
    if verbose > 0:
        print("{} lines loaded".format(
            str(len(conll_corpus)), filename))
    return conll_corpus


# @verbose
def split_list(a_list, proportion, verbose=0):
    """
    types: (list, tuple) -> tuple
    structure: (list[list[str]], tup) -> tuple(list, list, list)
    args:   proportion: output lists proportion
    Splits a list into a tuple containing 3 lists of precise proportions
    """
    if verbose > 0:
        print("Splitting list with proportions: {}".format(str(proportion)))
    first_list = a_list[:int(len(a_list) * proportion[0])]
    second_list = a_list[
        int(len(a_list) * proportion[0]):int(len(a_list) *
                                             proportion[0] + len(a_list) * proportion[1])]
    if verbose > 0:
        print("list splitted in 3 sublists of lengths: {} and {}".format(
            str(len(first_list)), str(len(second_list))))
    return (first_list, second_list)


def split_conll(filename, randomize=False, proportion=(0.9, 0.1), verbose=0):
    """
    types: (str) -> None
    structure: ("file name") => writes 3 output files
    Reads a conll file and splits it into 3 output files
    filename.train, filename.dev, filename.test
    """

    conll_cont = read_conll(filename, verbose)
    if randomize:
        conll_cont = random.shuffle(conll_cont)
    (train, test) = split_list(conll_cont, proportion, verbose)
    print(len(train))
    print(len(test))
    # trainfile = open(filename + ".train", 'w')
    # testfile = open(filename + ".test", 'w')
    # for sentence in train:
    #     for word in sentence:
    #         trainfile.write(word)
    #     trainfile.write("\n")
    # for sentence in test:
    #     for word in sentence:
    #         testfile.write(word)
    #     testfile.write("\n")
    # trainfile.close()
    # testfile.close()


def conll_list(filename, randomize=False, proportion=(1.0, 0.0)):
    """
    types: (str) -> list
    structure: ("file name") => list of conll lines
    Creates a list containing conll examples in lists
    (modded method)
    """

    conll_cont = read_conll(filename)
    if randomize:
        conll_cont = random.shuffle(conll_cont)
    (examples, _) = split_list(conll_cont, proportion)
    return examples


def read_embeddings(filename, verbose=0):
    """
    read embeddings
    """
    embedding_index = {}
    embedding_file = open(filename, 'r')
    # header = list(map(int, embedding_file.readline().strip().split(' ')))
    for line in embedding_file:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embedding_index[word] = coefs
    embedding_file.close()
    return embedding_index
