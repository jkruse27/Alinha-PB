import os
import sys
import string

class GramaticalClass:
	JAR = "lematizador.jar"
	text_file = "sentence.txt"
    
	#Gets the classes of the words in the sentence and stores it in sentences

	def __init__(self, sentence):
		self.sentences = '' 
		self.bases = ''
		sentence = sentence.translate(str.maketrans('', '', string.punctuation))
		arq = open(self.text_file, 'w')
		arq.write(sentence)
		arq.close()
		base_dir = '.'
		if hasattr(sys, '_MEIPASS'):
		    base_dir = os.path.join(sys._MEIPASS)

		os.system("mv " + self.text_file, os.path.join(base_dir,"LematizadorJava/lematizador"))
		os.chdir(os.path.join(base_dir,"LematizadorJava/lematizador"))
		os.system("java -jar " + self.JAR + " " + self.text_file)
		a = open(self.text_file+".tagged", "r")
		k = ""
		for i in a:
			self.sentences += i
		a.close()
		a = open(self.text_file+".out", "r")
		k = ""
		for i in a:
			self.bases += i
		a.close()
		os.chdir("cd -")

	# Returns the marked sentence
	def getSentences(self):
		return self.sentences

	# Returns the gramatical class for the Nth word
	def getClass(self, N):
		try:
			return self.sentences.split()[N].split("_")[1]
		except:
			return 0

	def getBase(self, N):
		try:
			return self.bases.split()[N].split("/")[1]
		except:
			return 0
