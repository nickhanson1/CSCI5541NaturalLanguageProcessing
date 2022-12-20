# CSCI 5541 Natural Language Processing

This repository is a collection of all of my assignments from the course CSCI 5541: Machine Learning in the spring of 2022. All homeworks were written in Python. Each folder is one homework assignment, 
possible consisting of multiple python files. The assignments are as follows:

### HW2/regex.py
A very rudimentary program that mimics "Eliza", a chatbot from the 1990s. The purpose was to practice creating regex patterns.

### HW3/spellchecker.py
Implements a spellchecker by tokenizing the input text and using the Hedit distance to determine which words are spelled incorrectly (with reference to a pregenerated list of words).

### HW4/classifier.py
Implements an N-Gram language modeler. Takes in input text from an author and creates a probobalistic model with 2- and 3-grams, then generates new text based off of the input.

### HW5/hmm_viterbi.py, HW5/hmm_model_build.py, HW5/hmm_sequence
These three files create a hidden Markov model in order to tag a sentance with its parts of speech, based off of pre-taged speech (the Brown corpus). 
hmm_model_build creates the initial model based off of the Brown corpus. hmm_sequence takes a model and a tagged sequence and returns the probability that
the sequene has that tagging, based off the input model. Finally, hmm_viterbi takes a model and an untagged sentence and uses the Viterbi algorithm to 
calculate the most probabilistically likely tag sequence for  the input.

### HW6/visualize.py
This takes a .wav file of speech, chunks the sound file and discretizes it, applies a Fourier transform to obtain the frequency of speech, and converts this data
to an image to visualize the speech.


### HW7/parser.py
This takes in a context free grammar and a word in the language of this grammar as an input, and creates all possible syntax trees for that sentence using the 
Earley algorithm.
