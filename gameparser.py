"""
This file stores functions for normalising player input.
Shouldn't be edited during development (unless something drastic needs changing)
"""

import string

# List of "unimportant" words (feel free to add more)
skip_words = ['a', 'about', 'all', 'an', 'another', 'any', 'around', 'at',
              'bad', 'beautiful', 'been', 'better', 'big', 'can', 'every', 'for',
              'from', 'good', 'have', 'her', 'here', 'hers', 'his', 'how',
              'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
              'like', 'little', 'main', 'me', 'mine', 'more', 'my', 'now',
              'of', 'off', 'oh', 'on', 'please', 'small', 'some', 'soon',
              'that', 'the', 'then', 'this', 'those', 'through', 'till', 'to',
              'towards', 'until', 'us', 'want', 'we', 'what', 'when', 'why',
              'wish', 'with', 'would']


def filter_words(words, skip_words):
    
    filtered_list = []
    for word in words:
        if not (word in skip_words):
            filtered_list.append(word)
            
    return filtered_list

    
def remove_punct(text):

    no_punct = ""
    for char in text:
        if not (char in string.punctuation):
            no_punct = no_punct + char

    return no_punct


def normalise_input(user_input):

    no_punct = remove_punct(user_input).lower()
    stripped = no_punct.strip()
    split_list = stripped.split()
    normalised_input = filter_words(split_list, skip_words)

    return normalised_input
