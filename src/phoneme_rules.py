# Class responsible for applying all the phonetic translations and
# simplifications that are invariable (do not need the probabilistic
# analysis)

class PhonemeRules:
	vogais = []

	def __init__(self):
		self.a = ["a", "á", "â", "ã"]
		self.o = ["o", "ó", "ô", "õ"]
		self.e = ["e", "é", "ê"]
		self.i = ["i", "í"]
		self.u = ["u", "ú"]
		self.vogais = self.a+self.e+self.i+self.o+self.u
		self.ponctuation = ["'",'"', ".", ",", ":", ";", "(", ")", "!", "?", "{", "}", "[", "]"]

	# Simplifies the words so that each character corresponds to
	# one single phoneme and each digraph only correspond to one
	# phoneme too (U_EXC representa o caso em que ha letra 'u' como 
	# exceção, ou seja, 'qui', 'gui', 'que', 'gue' em que o 'u' é pronunciado)

	# Receives word String and returns this word with unicharacters

	def simplify_word(self, word, U_EXC=False):
		new_word = ""
		size = len(word)
		word = word.lower()
		for i, c in enumerate(word):	
			# ----- Desconsidera 'h's -------#
			if(c == 'h'):
				pass

			# ----- Determina casos em que 'u' é ou não pronunciado e o 'q' e 'g' são /k/ e /zh/ ou /k/ e /g/ respectivamente ------- #
			elif(i <= size - 2 and c == 'g' and word[i+1] == 'u' and word[i+2] not in self.a and word[i+2] not in self.o):
				new_word += '|'
			elif(i > 0 and i < size - 1 and c == 'u' and word[i-1]=='g' and word[i+1] in self.vogais and word[i+1] not in self.a and word[i+1] not in self.o and not U_EXC):
				pass
			elif(i < size - 2 and c == 'q' and word[i+1] == 'u' and word[i+2] not in self.a and word[i+2] not in self.o):
				new_word += '['
			elif(i > 0 and i < size - 1 and c == 'u' and word[i-1]=='q' and word[i+1] in self.vogais and word[i+1] not in self.a and word[i+1] not in self.o and not U_EXC):
				pass

			# ----- Determina casos em que a sequencia 'xc' ou 'sc' ou 'sç' são apenas 1 fonema 
			elif((c == 'c' or c == 'ç') and i < size-1 and i > 0 and word[i-1] == 's' and (word[i+1] in self.i or word[i+1] in self.e)):
				pass
			elif((c == 'c' or c == 'ç') and i < size-1 and i > 0 and word[i-1] == 'x' and word[i+1] in self.vogais):
				pass
			elif(i < (size - 2) and c == 'x' and (word[i+1] == 'c' or word[i+1]=='ç') and word[i+2] in self.vogais):
				new_word += '$'
			elif(c == 'ç'):
				new_word += '$'

			# ----- Subsitui 'ch', 'nh' e 'lh' por 1 fonema só ------ #
			elif(i < (size - 1) and c == 'l' and word[i+1] == 'h'):
				new_word += '!'
			elif(i < (size - 1) and c == 'n' and word[i + 1] == 'h'):
				new_word += '@'
			elif(i < (size - 1) and c == 'c' and word[i + 1] == 'h'):
				new_word += '%'
		
			# ----- Substitui 'ss' e 'rr' por 1 fonema só ----- #
			elif(i < (size - 1) and c == 's' and word[i + 1] == 's'):
				new_word += '$'
			elif(i >= 1 and c == 's' and word[i - 1] == 's'):
				pass
			elif(i < (size - 2) and c == 'r' and word[i + 1] == 'r'):
				new_word += '^'
			elif(i >= 1 and c == 'r' and word[i - 1] == 'r'):
				pass
		
			# ----- Retira todas as pontuações que tem na palavra ----- #
			elif(word[i] in self.ponctuation):
				pass		
			
			# ----- Qualquer outro grafema se mantem ----- #
			else:
				new_word += word[i]

		return new_word


	# Method responsible for applying the phonetic rules to individual
	# characters in a word.

	# Receives the word String and an int with the characters position
	# Returns the characters correspondent phoneme or null in case the
	# probabilistic analysis is required

	def apply_rule(self, words, char_num):
		word = words.getSimplified()
		isSandi = words.getIsSandi()
		size = len(word)
		char = word[char_num]
		ret = char
	
		# ----- Conversões diretas, independentes de contexto ------ #
		if (char == 'â'):
			ret = 'aN' 

		elif (char == 'à'):
			ret = 'a'

		elif (char == 'á'):
			ret = 'a'

		elif (char == 'b'):
			ret = 'b'

		elif (char=='ê'):
			ret = 'e'

		elif (char == 'f'):
			ret = 'f'
		
		elif (char == 'í'):
			ret = 'i'

		elif (char == 'j'):
			ret = 'zh'
		
		elif (char == 'ó'):
			ret = 'oh'

		elif (char == 'ô'):
			ret = 'o'

		elif (char == 'p'):
			ret = 'p'

		elif (char == 'q'):
			ret = 'k'
		
		elif (char == 'ú'):
			ret = 'u'

		elif (char == 'v'):
			ret = 'v'

		elif (char == '|'):
			ret = 'g'

		elif (char == '['):
			ret = 'k'
		
		elif (char == '%'):
			ret = 'sh'
		
		elif (char == '!'):
			ret = 'lh'
		
		elif (char == '$'):
			ret = 's'
		
		elif (char == '@'):
			ret = 'nh'

		elif(char == '^'):
			ret = 'r'
		
		# ---------------------------------------------- #	
		# ----- Conversões dependentes de contexto ----- #
	
		# -- Consoantes -- #

		elif (char == 'c'):
			if (char_num < size - 1 and (word[char_num + 1] == 'e' or word[char_num + 1] == 'i' or word[char_num + 1] == 'é' or word[char_num + 1] == 'ê' or word[char_num + 1] == 'í')):
				ret = 's'
			else:
				ret = 'k'

		elif (char == 'd'):
			if (char_num < size - 1 and (word[char_num + 1] == 'i' or word[char_num + 1] == 'í')):
				ret = 'dZ'
			elif (char_num < size - 1 and word[char_num + 1] == 'n'):
				ret = 'dZ'
			elif (char_num < size - 1 and word[char_num + 1] == 'e'):
				if (word.find('de') == size - 2):
					ret = 'dZ'
				else:
					ret = 'd'
			else:
				ret = 'd'
		
		elif (char == 'g'):
			if (char_num<size-1 and (word[char_num+1] in self.i or word[char_num+1] in self.e)):
				ret = 'zh'
			else:
				ret = 'g'
		
		elif (char == 'l'):
			if (char_num == size-1):
				ret = 'U'
			elif ((char_num < size - 1 and word[char_num + 1] not in self.vogais) or char_num==size-1):
				ret = 'U'
			else:
				ret = 'l'

		elif (char == "m" or char == "n"):
			if (char=='m' and char_num != 0 and char_num==size-1 and word[char_num-1]=='a'):
				ret='U'
			#elif (char_num!=0 and char_num < size-1 and word[char_num-1] in self.vogais and word[char_num+1] not in self.vogais):
			#	ret = 'N'
			#elif (char_num == size - 1):
			#	ret = 'N'
			else:
				ret = char

		elif(char == 'r'):
			if(char_num == 0):
				ret = 'r'
			else:
				ret = 'R'
		
		elif (char == 's'):
			if (char_num < size-1 and char_num > 0 and word[char_num-1] in self.vogais and word[char_num+1] in self.vogais):
				ret = 'z'
			elif (char_num==size-1):
				ret = 'S'
			elif (char_num==4 and word.find("trans")==0):
				if(word[char_num+1] in self.vogais):
					ret = 'Z'
				else:
					ret = 'S'
			elif (char_num<size-1 and word[char_num+1] not in self.vogais):
				ret = 'S'
			elif (char_num>0 and word[char_num-1] not in self.vogais):
				ret = 's'
			elif (char_num==0):
				ret = 's'
			elif (char_num >= 1 and char_num < size - 1 and word[char_num - 1] in self.vogais and word[char_num + 1] in self.vogais):
				ret = 'z'
			else:
				ret = 'S'
		
		elif (char == 't'):
			if (char_num < size-1):
				if (word[char_num + 1] == 'i' or word[char_num + 1] == 'í'):
					ret = 'tS'
				elif (word[char_num + 1] == 'n'):
					ret = 'tS'
				elif (word.find('tes') == size-3):
					ret = 'tS'
				elif (word[char_num + 1] == 'e'):
					if (word.find('te') == size - 2):
						ret = 'tS'
					else:
						ret = 't'
				else:
					ret = 't'

		elif (char == 'x'):
			if (char_num >= 1 and char == 'x' and word[char_num - 1] == 'a'):
				ret = 'sh'
			elif (char_num >= 1 and char == 'x' and word[char_num - 1] == 'i'):
				ret = 'sh'
			elif (char_num < size - 3 and char_num >= 1 and word[char_num-1:char_num+1] == "ax" and word[char_num+2] not in self.vogais):
				if (word[char_num+2] != 'l' and word[char_num+2] != 's' and word[char_num+1] == 'e'):
					ret = 'sh'
				elif (word[char_num+1] == 'i'):
					ret = 'sh'
				else:
					ret = 'ks'
			elif (char_num < size-1 and char_num > 0 and word[char_num-1]=='u' and word[char_num+1]=='a'):
				ret = 'sh'
			elif (char_num == size - 2 and (word[char_num-1:char_num+2]=='axe' or word[char_num-1:char_num+2] == "axe")):
				ret = 'sh'
			elif (char_num < size - 4 and char_num > 0 and word[char_num-1:char_num+3] == "axei" and (word[char_num+3] not in self.vogais)):
				ret = 'sh'
			elif (char_num > 0 and char_num < size - 2 and word[char_num-1:char_num+2] == "axa"):
				ret = 'sh'
			elif (char_num > 0 and char_num < size - 4 and word[char_num-1:char_num+1] == 'ax' and word[char_num+1] in self.vogais and word[char_num+2] == 'i'):
				ret = 'ks'
			elif (char_num > 0 and char_num < size - 4 and word[char_num-1:char_num+2] == 'axi' and wprd[char_num+2] in self.vogais):
				ret = 'ks'
			elif (char_num > 0 and char_num < size - 4 and word[char_num-1:char_num+3] == 'axis'):
				ret = 'ks'
			elif (char_num == size - 1 and word[char_num-1:char_num+1] == "ax"):
				ret = 'ks'
			elif (char_num >= 2 and char_num < size - 2 and word[char_num-1:char_num+1] == 'ix' and word[char_num-2] in self.vogais and word[char_num+2] in self.vogais):
				ret = 'sh'
			elif (char_num >= 1 and char_num < size - 1 and word[char_num-1:char_num+1] == 'ix' and word[char_num+1] in self.vogais):
				ret = 'sh'
			elif (char=='x' and char_num!=0 and char_num<size-1 and word[char_num-1]=='e' and word[char_num+1] not in self.vogais):
				ret = 's'
			elif (char_num!=0 and char_num<size-1 and word[char_num-1:char_num+2]=='exa'):
				ret = 'z'
			elif (char=='x' and char_num==size-1 and word[char_num-1]=='e'):
				ret = 'ks'
			elif (char=='x' and char_num!=0 and char_num<size-1 and word[char_num-1]=='e' and word[char_num+1] in self.vogais):
				ret = 'z'
			elif (char == 'x' and char_num < size - 1 and word[char_num + 1] in self.vogais):
				if (char_num == 1 and char == 'x' and word[char_num - 1] == 'e'):
					ret = 'z'
				elif (word[0] == 'h' and char == 'x' and word[char_num - 1] == 'e'):
					ret = 'z'
				elif (word[0:2] == "in" or word[0:3] == "pre" or word[0:2] == "co"):
					ret = 'z'
				else:
					ret = 'ks'
			else:
				ret = 'sh'

		elif (char == 'z'):
			if (char_num == size-1):
				ret = 'S'
			elif (char_num < size - 1 and word[char_num+1] not in self.vogais):
				ret = 's'
			else:
				ret='z'
		

		# -- Vogais -- #
		
		elif (char=='a'):
			if(isSandi and char_num == size-1):
				ret = ''
			elif(char_num==size-2 and (word[char_num+1]=='m' or word[char_num+1]=='n')):
				if (char_num<=words.getTonic()):
					ret = 'aN'
				else:
					ret = 'AN'
			elif (char_num <= words.getTonic()):
				ret = char
			else:
				ret = char.upper()
		
		elif (char=='ã'):
			if(char_num<=words.getTonic()):
				ret = 'aN'
			else:
				ret = 'AN'
		
		elif (char == 'é'):
			if(char_num < size-1 and word[char_num+1] in ['m', 'n']):
				ret = 'e'
			else:
				ret = 'eh'
		
		elif (char == 'e'):
			if (word.find('eia') == char_num):
				ret = 'e'
			elif (char_num < size - 1 and (word[char_num + 1] == 'm' or word[char_num + 1] == 'n')):
				if (char_num <= words.getTonic()):
					ret = 'e'
				else:
					ret='E'
			elif(char_num > 0 and char_num==size-1 and char_num != words.getTonic() and word[char_num-1] in ['t', 'd']):
				ret = ''
			elif (char_num==size-1 or (char_num==size-2 and word[char_num+1]=='s')):
				if (char_num == words.getTonic()):
					ret = 'i'
				else:
					ret='I'
			elif (char_num==words.getTonic() and char == 'e' and words.getIsExc()==0):
				if(word[-1] == 'a' or word[-2:]=='as'):
					ret = 'eh'
				else:
					ret = 'e'
			elif (char_num <= words.getTonic()):
				ret = char
			else:
				ret = char.upper()
		
		elif (char == 'i'):
			if (char_num <= words.getTonic()):
				ret = char
			else:
				ret = char.upper()
			
		elif (char=='o'):
			if (char_num==size-1 or (char_num==size-2 and word[-2:] == 'os')):
				if (char_num==words.getTonic()):
					ret = 'u'
				else:
					ret = 'U'
			elif (char_num < size - 1 and (word[char_num + 1] == 'm' or word[char_num + 1] == 'n')):
				if (char_num <= words.getTonic()):
					ret = 'o'
				else:
					ret='O'
			elif (char_num == word.find('oia')):
				if (char_num <= words.getTonic()):
					ret = 'oh'
				else:
					ret = 'O'
			elif (char_num==words.getTonic() and char == 'o' and words.getIsExc()==0):
				if(word[-1] == 'a' or word[-2:]=='as'):
					ret = 'oh'
				else:
					ret = 'o'
			elif (char_num <= words.getTonic()):
				ret = char
			elif (char_num == size - 2 and word[size-1] == 'l'):
				ret = 'oh'
			else:
				ret = char.upper()
			
		elif (char=='õ'):
			if (char_num<=words.getTonic()):
				ret = 'oN'
			else:
				ret = 'ON'
		
		elif (char == 'u'):
			if (char_num > 0 and word[char_num - 1] in ['q','g']):
				ret = 'U'
			elif (char_num > 0 and word[char_num - 1] == 'o' and words.getTonic() != char_num):
				ret = 'U'
			elif (char_num <= words.getTonic()):
				ret = char
			else:
				ret = char.upper()
	
		return ret
