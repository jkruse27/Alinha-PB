from hash_map import *
import sys
import re, os
from phoneme_rules import *
from Word import *
from GramaticalClass import *
import string


class Word:
	acentos = ["á", "í", "ú", "é", "ó", "â", "ê", "ô"]
	til = ["ã", "õ"]
	vogais = ["a", "i", "u", "e", "o"]+acentos+til
	oxitonas = ["a", "e", "o", "em", "as", "es", "os", "ens", "am", "ans"]
	phoneme_rules = None
	exceptions = None
	homographs = None
	verbs = None
	gramatica = None
	base_dir='.'

	def __init__(self, word, pos, gramatica=None):

		self.isExcept = 0
		self.pos = pos
		self.word = word.lower()
		self.simplified = ''
		self.tonic = -1
		self.classe = ""
		self.convertion = ''
		self.time = ''
		self.base = ''
		self.isSandi = False
		base_dir='.'

		if hasattr(sys, '_MEIPASS'):
		    base_dir = os.path.join(sys._MEIPASS)
	
		if(Word.homographs == None):
			Word.homographs = ExceptionHashMap(os.path.join(base_dir, "Dictionaries/Homographs.json"))
			Word.homographs.create_hash()
		if(Word.verbs == None):
			Word.verbs = ExceptionHashMap(os.path.join(base_dir, "Dictionaries/Verbs.json"))
			Word.verbs.create_hash()
		if(Word.exceptions == None):
			Word.exceptions = ExceptionHashMap(os.path.join(base_dir,"Dictionaries/Exceptions.json"))
			Word.exceptions.create_hash()
		if(Word.phoneme_rules == None):
			Word.phoneme_rules = PhonemeRules()
		if(Word.gramatica == None and gramatica != None):
			Word.gramatica = gramatica			

	@staticmethod
	def update_exceptions():
		base_dir='.'
		Word.homographs = ExceptionHashMap(os.path.join(base_dir, "Dictionaries/Homographs.json"))
		Word.homographs.create_hash()
		Word.verbs = ExceptionHashMap(os.path.join(base_dir, "Dictionaries/Verbs.json"))
		Word.verbs.create_hash()
		Word.exceptions = ExceptionHashMap(os.path.join(base_dir,"Dictionaries/Exceptions.json"))
		Word.exceptions.create_hash()


	def convert_word(self):
		conversion = ''
		#if(Word.homographs.part_or_total(self.word) == 1):
		#	conversion = Word.homographs.conv_hom(self)
		#elif(Word.exceptions.part_or_total(self.word) == 1):
		if(Word.exceptions.part_or_total(self.word) == 1):
			conversion = Word.exceptions.get_phoneme(self.word)
		elif(Word.exceptions.part_or_total(self.word) == 2):
			self.simplified = Word.phoneme_rules.simplify_word(self.word)
			self.find_tonic()
			conversion = ''
			first_part, second_part = Word.exceptions.get_range_of_part(self.word)
			exception_part = Word.exceptions.get_phoneme(self.word)
			for j in range(first_part):
				char = Word.phoneme_rules.apply_rule(self, j)
				if(char == None):
					conversion += '-'
				else:
					conversion += char
			conversion += exception_part
			for j in range(second_part, len(self.simplified)):
				char = Word.phoneme_rules.apply_rule(self, j)
				if(char == None):
					conversion += '-'
				else:
					conversion += char
		else:
			if (Word.verbs.part_or_total(self.base) == 1):
				self.simplified = Word.phoneme_rules.simplify_word(self.word, U_EXC=True)
			else:
				self.simplified = Word.phoneme_rules.simplify_word(self.word)
			self.find_tonic(is_simplified=True)
			for j, e in enumerate(self.simplified):
				char= Word.phoneme_rules.apply_rule(self, j)
				if char != None:
					conversion += char
				else:
					conversion += '-'

		self.conversion = conversion
		return conversion
		
				
	# Retorna a posição da tônica em uma sílaba baseada na prioridade das vogais
	def priority(self, vog2, ox = False):
		a=-1
		if(len(vog2) == 1):
			a = 0
		elif('a' in vog2):
			a = vog2.rfind('a')
		elif('eo' in vog2):
			a = vog2.find('eo') + 1
		elif('oe' in vog2):
			a = vog2.find('oe') + 1
		elif('o' in vog2):
			a = vog2.rfind('o')
		elif('e' in vog2):
			a = vog2.rfind('e')
		elif('ui' in vog2):
			a = vog2.rfind('u')
		elif('i' in vog2):
			a = vog2.rfind('i')
		else:
			a = vog2.rfind('u')
		
		return a

	#Sets the position of the tonic in the word
	def find_tonic(self, is_simplified=False):
		word=''
		if(is_simplified):
			word = self.simplified
		else:
			word = self.word	
	
		acento, til, vogal = -1,-1,-1
		v = 0 
		for j, i in enumerate(word):
			if i in self.acentos:
				acento = j
			if i in self.til:
				til = j
			if i in self.vogais:
				vogal = j
				v += 1
	
		# Caso tenha alguma letra acentuada, ela é a tônica
		if (acento != -1):
			self.tonic = acento
			return self
		# Caso tenha alguma letra com til, ela é a tônica
		elif (til != -1):
			self.tonic = til
			return self
		# Caso tenha apenas uma vogal, ela é a tônica
		elif (v == 1):
			self.tonic = vogal
			return self

		# Caso não haja letra acentuada, nem til aplicamos a regra de acentuacao inversa
		if self.tonic == -1:
			# Pega a última sequência de vogais e a penúltima
			vog1, vog2 = "", ""
			p = ""
			pos1, pos2 = -1, -1
			time1 = True
			time2 = False
			for i, j in reversed(list(enumerate(word))):
				if (j in self.vogais and time1):
					vog1 = j + vog1
					pos1 = i 
				elif (j in self.vogais and time2):
					vog2 = j + vog2
					pos2 = i
				else:
					if(time1):
						if (len(vog1) != 0):
							time1 = False
							time2 = True
						else:
							p = j + p
					else:
						if (len(vog2) != 0):
							break
			vog1 = vog1+p
			# Se a sequência final corresponder a um dos casos em que uma oxítona seria acentuada, 
			# então a palavra é paroxitona
			if (vog1 in self.oxitonas):
				if(vog2[-1] in ['i','u'] and word[pos2+len(vog2)] not in self.vogais and word[pos2+len(vog2)+1] not in self.vogais):
					self.tonic = pos2 + len(vog2) - 1
				else:
					self.tonic = pos2 + self.priority(vog2)
			else:
				if(len(vog1) >= 1 and vog1[-1:] in self.oxitonas):
					self.tonic = pos1 + self.priority(vog1[:-1])
				elif(len(vog1) >= 2 and vog1[-2:] in self.oxitonas):
					self.tonic = pos1 + self.priority(vog1[:-2])
				elif(len(vog1) >= 3 and vog1[-3:] in self.oxitonas):
					self.tonic = pos1 + self.priority(vog1[:-3])
				else:
					if(len(vog1) == 1):
						self.tonic = pos1
					else:
						v = 0
						for i in vog1:
							if(i in self.vogais):
								v += 1
						if(v == 1):
							self.tonic = pos1 + self.priority(vog1)
						else:
							if(vog1[-1] not in self.vogais and vog1[-2] in ['i','u'] and vog1[-1] != 's'):
								self.tonic = pos1 + len(vog1[:-2])
							else:
								self.tonic = pos1 + self.priority(vog1)	
		return self	
	def getSimplified(self):
		return self.simplified

	def getWord(self):
		return self.word

	def setWord(self, word):
		self.word = word

	def setClass(self):
		self.classe = Word.gramatica.getClass(self.pos)

	def getClass(self):
		return self.classe
    
	def getTonic(self):
		return self.tonic

	def getType(self):
		return self.type

	def setBase(self):
		self.base = Word.gramatica.getBase(self.pos)

	def getBase(self):
		return self.base

	def getIsExc(self):
		return self.isExcept

	def setIsExc(self):
		self.isExcept = Word.homographs.is_tonic_exception(self.base)

	def getIsSandi(self):
		return self.isSandi

	def setIsSandi(self, next_word=None):
		if(next_word == None):
			self.isSandi = False
		else:
			if(self.word[-1] == 'a' and self.tonic != len(self.word)-1):
				if(next_word.getWord()[0] in self.vogais and next_word.getTonic() != 0):
					self.isSandi = True
				else:
					self.isSandi = False
			else:
				self.isSandi = False


