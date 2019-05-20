#!/usr/bin/python
# -*- encoding: utf-8 -*-
# A rhyming slang generator mimicing the style of Cockney Rhyming Slang. Hav'a butcher's at the code below. 
# Usage: >>> python cockneyRhymer.py inputText.txt outputText.txt
#        >>> python cockneyRhymer.py -r "You're having a laugh aren't you?"
import sys
import codecs
import requests
import json
import random
import inflect
from nltk import word_tokenize, pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from bnc import bigrams
from operator import itemgetter

RHYME_URL = "https://api.datamuse.com/words?rel_rhy="   # Datamuse Rhyme Words API endpoint

LEM = WordNetLemmatizer()     # Instantiate nltk's WordNet lemmatizer object

INF = inflect.engine()        # Instantiate and Inflect object for generating noun plurals

# For a given word, retrieve rhyming words via HTTP GET request to the awesome Datamuse API. Return list of matching rhyme words.
def get_rhyme(word):
    # HTTP GET request to Datamust API via requests library. Returns a JSON response.
    response = requests.get("{}{}".format(RHYME_URL, word.lower()))
    rhyme_words = []
    if response.ok:
        rhymes = json.loads(response.text)

        # Parse JSON reponse from Datamuse API
        for rhyme_word in rhymes:
            rhyme_words.append(rhyme_word['word'])
            
    else: print("Connection Error: Check Internet Connection."); sys.exit(1)
   
    return rhyme_words

# Extract first found collocation already present in Datamuse API's response. Return collocation. 
# These collocations can be used as a backup if no match found to collocations in the BNC.
def get_rhyme_collocations(rhyme_words):
    rhyme_collocations = []
    for rhyme_word in rhyme_words:
        if ' ' in rhyme_word: rhyme_collocations.append(rhyme_word.split(' '))
        else: continue

    return rhyme_collocations

# For a given noun, find at matching collocation from noun-noun bigrams extracted from the British National Corpus. Return first matching bigram or 'none'.
def get_collocations(rhyme_words):
    collocations = []
    for rhyme_word in rhyme_words:
        for word in bigrams:
            # Look for match between rhyming word and second word in a BNC noun-noun collocation
            if word[0].decode('utf8') == rhyme_word: 
                print("rhymes with {}, {} {} ({})".format(word[0], word[1], word[0], word[2]))
                collocations.append([word[0], word[1], int(word[2])])
            else: continue
    
    return collocations

# Perform word stemming or lemmatization. Returns stemmed words or lemmas 
def stem(word):

    # Use NLTK lemmatization. Could also use NLTK's PorterStemmer as an alternative option.
    stem = LEM.lemmatize(word)

    return stem

# Process the user's text with NLTK to extract nouns from the text. Return a list of nouns.
def nlp(text):
    # Tokenize text into words, returns list of words
    tokens = word_tokenize(text)        

    # Apply Parts-of-Speech tagging, returning tagged tuples for each word
    tagged_tokens = pos_tag(tokens) 

    # Extract only nouns from the tagged text e.g. NN, NNP and NNPS tags
    # Perform word stemming or lemmatization, retain whether or not original noun was singular or plural.
    nouns = []
    for tagged_token in tagged_tokens:
        if 'NN' in tagged_token[1]: 
            if 'NNS' in tagged_token[1] or 'NNPS' in tagged_tokens[1]: 
                if INF.singular_noun(tagged_token[0]):
                    if INF.singular_noun(tagged_token[0]) not in tagged_token[0] or stem(tagged_token[0]) == tagged_token[0]:
                        nouns.append([tagged_token[0], 'irr_plural'])
                    else:
                        nouns.append([stem(tagged_token[0]), 'plural'])
            else: nouns.append([stem(tagged_token[0]), 'singular'])

    return nouns

# Convert the user's input text into cockney-style rhyming text. Return cockney rhyming text.
def build(input_text, mode):
    # Extract nouns from the user's input text string
    nouns = nlp(input_text)

    # Look for nouns with rhyming word matches
    cockney_text = input_text
    for noun in nouns: 
        rhyme_words = get_rhyme(noun[0])

        # Check rhyming words are not substrings of original noun e.g. 'ball' rhymes with 'football'
        for rhyme_word in rhyme_words:
            if rhyme_word in noun: del rhyme_words[rhyme_words.index(rhyme_word)]    # delete rhyme_word from the list

        # Find collocation matches in BNC bi-grams with the list of rhyming words
        cockney_nouns = get_collocations(rhyme_words)

        # If no matches found within the BNC, look for collocations already existing within the list of rhyming words
        if cockney_nouns == None: 
            cockney_nouns = get_rhyme_collocations(rhyme_words)

        # Sort collocations based on BNC scores (how common the collocation is within the BNC data)
        if cockney_nouns: 
            cockney_nouns = sorted(cockney_nouns, key=itemgetter(2), reverse=True)

            # Select a random match from the list of BNC collocations
            if mode: 
                cockney_noun = random.choice(cockney_nouns)
            else: 
                # Select the collocation with the highest BNC frequency score 
                cockney_noun = cockney_nouns[0]

            # Replace original noun in user's input text with cockney rhyming noun
            # Generate plural of cockney noun if replacing an original plural noun
            if cockney_noun: 
                if noun[1] == 'plural': cockney_text = cockney_text.replace(INF.plural_noun(noun[0]), INF.plural_noun(cockney_noun[1]))
                else: 
                    if noun[1] == 'irr_plural': cockney_text = cockney_text.replace(noun[0], INF.plural_noun(cockney_noun[1]))
                    else: cockney_text = cockney_text.replace(noun[0], cockney_noun[1])

    return cockney_text

# Main
def main():
    mode = sys.argv[1]
    io_mode = sys.argv[2]

    output_filepath = None
    input_filepath = None
    output_text = None
    input_text = None

    # Handle user input. Check input mode and read input data from file if given
    # User options: 
    #   -r for selecting random matches for rhyming nouns
    #   -b for selecting Datamuse's best scored matched for rhyming nouns  
    random = False
    if mode == '-r': random = True
    elif mode == '-b': random = False
    else: print("Error: Select -r or -b options"); sys.exit(1)

    if io_mode == "-f": 
        input_filepath = sys.argv[2]
        input_text = open(input_filepath, 'r').read()     # Read input text from given filepath
        output_filepath = sys.argv[3]
    else:
        input_text = sys.argv[2]                          # Read input text from CLI

    # Convert user's input text to cockney rhyming text
    output_text = build(input_text, random)

    # Handle script output. Print output text to a file if given otherwise print to stdout
    if output_filepath is not None:
        with open(output_filepath, 'w') as foutput:
            foutput.write(output_text.encode('utf8'))
    else: print(output_text)

if __name__ == '__main__':
    main() 