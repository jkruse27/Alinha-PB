from hash_map import *
import sys
import re
from phoneme_rules import *
from Word import *
#from GramaticalClass import *
import string

class Conversor:
	def convert_sentence(self, sentence):
	
		sentence = sentence.replace('-', ' ')
		sentence = sentence.translate(str.maketrans('', '', string.punctuation))
		converted_sentence = ''
		#gramatica = GramaticalClass(sentence)
		
		lista = [i.lower() for i in re.findall(r"[\w]+", sentence)]
		words = [Word(palavra, pos) for pos, palavra in enumerate(lista)]
		words = list(map(lambda x: x.find_tonic(), words))

		for num, word in enumerate(words):
			#word.setClass()
			#word.setBase()
			word.setIsExc()
			word.find_tonic()
			if(num != len(words)-1):
				word.setIsSandi(words[num+1])
			conversion = word.convert_word()
			if(word.getIsSandi()):
				converted_sentence += conversion
			else:
				converted_sentence += conversion + ' '


		return converted_sentence
