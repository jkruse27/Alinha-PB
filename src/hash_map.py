import os
import json
from phoneme_rules import *

# Class responsible for the exceptions dictionary

class ExceptionHashMap:

    # When initialized it requires the address where the 
    # hash map will be stored and recovered from

    def __init__(self, address):
        self.address = address
        #dic_s is for words that are exceptions by themselves
        self.dic_s = {}
        #dic_c is for words that are exceptions and their derivatives are exceptions too
        self.dic_c = {}

    # Returns the phoneme translation to a word in the case it is
    # in the exceptions dictionary

    def get_phoneme(self, word):
        ret = ""
        
        if(word in self.dic_s):
            return self.dic_s[word]
        for i in self.dic_c:
            if(i in word):
                ret = self.dic_c[i]
                break
        return ret
    
    
    # Adds another exception to the dictionary
    # Requires the word and it's translation and if it is simple or composite

    def add_exception(self, grapheme, phoneme, form):
        if(form.lower() == 'simple'):
            self.dic_s[grapheme.lower()] = phoneme
        else:
            self.dic_c[grapheme.lower()] = phoneme
    
    # Removes a word from the dictionary

    def remove_exception(self, word, form):
        if(form.lower() == 'simple'):
            if(word.lower() in self.dic_s):
                self.dic_s.pop(word.lower())
        else:
            if(word.lower() in self.dic_c):
                self.dic_c.pop(word.lower())

    
    # Creates the dictionary from the file in the address
    
    def create_hash(self):
        with  open(self.address, "r") as arq:
            self.dic_s = json.loads(arq.readline())
            self.dic_c = json.loads(arq.readline())
    
    # Stores the hash map in the file in the address

    def store_hash(self):
        with open(self.address, "w") as arq:
            arq.write(json.dumps(self.dic_s))
            arq.write("\n")
            arq.write(json.dumps(self.dic_c))

    # Returns the right conversion for homographs based on its gramatical class

    def conv_hom(self, word):
        ret = None
        try:
            if word.getClass() != "N":
                ret = self.dic_s[word.getWord()].split("/")[1]
            else:
                ret = self.dic_s[word.getWord()].split("/")[0]
        except:
            pass
        return ret

    # Finds if part of a word is  a exception or the whole word

    def part_or_total(self, word):
        if(word in self.dic_s):
            return 1
        for i in self.dic_c:
            if i in word:
                return 2
        return 0

    def getDictionary(self):
        return self.dic_s, self.dic_c
    #Returns the beggining and end of the part for which the exception applies

    def get_range_of_part(self, word):
        k = PhonemeRules() 
        for i in self.dic_c:
            l = k.simplify_word(i)
            if(l in word):
                a = word.find(l)
                return a, a+len(l)

    def is_tonic_exception(self, word):
        if word in self.dic_c:
            return 1
        return 0
