import os
from Parser import *
from Conversor import *
import sys
import re
import subprocess


base_dir = '.'
if hasattr(sys, '_MEIPASS'):
	base_dir = os.path.join(sys._MEIPASS)

TMP=os.path.join(base_dir, 'tmp/')

class TextConverter():
	
	# Retorna dicionario contendo a conversao das silabas foneticas para fonemas 
	def convert(self, text):
		v = []
		for i in text:
			if(i not in v):
				v.append(i)
		lexer = PhonemeLexer()

		with open(os.path.join(TMP,"dict"), "w") as f:
			for i in sorted(v):
				f.write("%s %s\n" %(i, re.sub(' +', ' '," ".join(map(lambda x: x.value, lexer.tokenize(i))).replace(",", ""))))
	
	
	# Cria um dicionario a partir do texto
	def create_dict(self, text):
		self.convert(text.split())
	
	# Cria um arquivo mlf
	def mlf(self, text, name):
		with open(os.path.join(TMP,"mlf.mlf"), "w") as f:
			f.write('#!MLF!#\n"*/%s"\n' %name.replace(".wav", ".lab"))
			for i in text:
				f.write("%s\n" %i)
			f.write(".\n")
		with open("%s" %name.replace(".wav", ".lab"), "w") as f:
			for i in text:
				f.write("%s\n" %i)

	def scp(self, name):
		with open(os.path.join(TMP,"audios.scp"), "w") as f:
			f.write("%s %s\n" %(name, name.replace(".wav", ".mfc")))
		with open(os.path.join(TMP,"mfc.matl"), "w") as f:
			f.write("%s\n" %name.replace(".wav", ".mfc"))

	def generate_textgrid(self, name, repl="", mul_text=False):
		l = repl.split()
		try:
			with open(os.path.join(TMP,"recog.out"), "r") as w:
				for i in w:
					if(i[0]=='"'):
						with open("%s" %i[1:-2].replace(".rec", ".lab"), "w") as f:
							count = 0
							new_file = []
							for j in w:
								if(j[0]=="."):
									break
								else:
									if(repl==""):
										f.write(j)
									else:
										m = j.split()
										if(m[2] != "sil" and m[2] != 'sp'):
											m[2] = l[count]
											count += 1
										if(m[2] == 'sp'):
											new_file[-1] = " ".join([i if j != 1 else m[1] for i,j in enumerate(new_file[-1].split())])
										else:
											new_file.append(" ".join(m))						 
							f.write('\n'.join(new_file))
			if(mul_text):
				self.multi_split(name.replace(".wav", ".lab"), name.replace(".wav", ".TextGrid"), os.path.join(TMP,"text1.out"), os.path.join(TMP,"text2.out"))
			else:
				self.lab_to_textgrid(name.replace(".wav", ".lab"), name.replace(".wav", ".TextGrid"))
		except:
			pass

	@staticmethod
	# Cria todos os arquivos necessarios para o alinhamento
	def perform_conversion(text, filename, in_format, out_format, aligner='HTK'):

		text1=text
		converter = Conversor()
		lexer = PhonemeLexer()
		parser = PhonemeParser()		

		if(in_format == 'graf'):
			text = converter.convert_sentence(text1)

		if(out_format == 'fonema'):
			# Converte para fonemas individuais
			text = re.sub(' +', ' '," ".join(map(lambda x: x.value, lexer.tokenize(text))).replace(",", ""))
		elif(out_format == 'silaba'):

			v = []
			# Marca tonicas com ','
			for palavra in text.split():
				for position, character in enumerate(reversed(palavra)):
					if(character in ['a', 'i', 'u', 'e', 'o']):
						tmp = list(palavra)
						tmp.insert(len(palavra) - position, ',')
						v.append("".join(tmp))
						break

			# Converte para silabas foneticas
			text = parser.parse(lexer.tokenize(" ".join(v)))
			#text = re.sub(' +', ' '," ".join(map(lambda x: x.value, lexer.tokenize(" ".join(v)))).replace(",", ""))
		elif(out_format == 'todos'):
			v = []
			# Marca tonicas com ','
			for palavra in text.split():
				for position, character in enumerate(reversed(palavra)):
					if(character in ['a', 'i', 'u', 'e', 'o']):
						tmp = list(palavra)
						tmp.insert(len(palavra) - position, ',')
						v.append("".join(tmp))
						break
			# Conversao em silabas foneticas eh salva em text1.out
			with open(os.path.join(TMP,"text1.out"), "w") as f:
				f.write(parser.parse(lexer.tokenize(" ".join(v))))
			# Conversao em palavras eh salva em text2.out
			with open(os.path.join(TMP,"text2.out"), "w") as tt:
				tt.write(text)

			text = re.sub(' +', ' '," ".join(map(lambda x: x.value, lexer.tokenize(text))).replace(",", ""))
		
		if(aligner == 'HTK' or aligner=='Kaldi'):
			text = text.split()
			text.insert(0, "sil")
			text.append("sil")
			text = " ".join(text)
		
		txt_cnv = TextConverter()		
		txt_cnv.create_dict(text)

		if(aligner == 'HTK'):
			txt_cnv.mlf(text.split(), filename)
			txt_cnv.scp(filename)
		elif(aligner == 'Kaldi'):
			with open(os.path.join(TMP,"train.lab"), "w") as f:
				f.write(text)
		return text

	@staticmethod
	def align(text, filename, in_format, out_format, aligner='HTK', hmmdefs=False, config=False):
		base_dir = '.'
		if hasattr(sys, '_MEIPASS'):
			base_dir = os.path.join(sys._MEIPASS)

		if(aligner == 'HTK'):
			if('win' not in sys.platform.lower()):
				subprocess.run([os.path.join(base_dir,"htk/bin.cpu/HCopy"), "-C", os.path.join(base_dir,"lib/config.parming"), "-S", os.path.join(TMP,"audios.scp")])
				if(hmmdefs):
					subprocess.run([os.path.join(base_dir,"htk/bin.cpu/HVite"), "-a", "-C", 
							os.path.join(base_dir,"lib/config"), "-H", os.path.join(base_dir,"models/hmm/hmmdefs"), 
							"-I", os.path.join(TMP,"mlf.mlf"), "-S", os.path.join(TMP,"mfc.matl"), "-i",
							os.path.join(TMP,"recog.out"), os.path.join(TMP,"dict"), os.path.join(TMP,"hmm_names")])
				else:
					subprocess.run([os.path.join(base_dir,"htk/bin.cpu/HVite"), "-a", "-C", \
							os.path.join(base_dir,"lib/config"), "-H", os.path.join(base_dir,"models/hmm/hmmdefs"), \
							"-I", os.path.join(TMP,"mlf.mlf"), "-S", os.path.join(TMP,"mfc.matl"), "-i", \
							os.path.join(TMP,"recog.out"), os.path.join(TMP,"dict"), os.path.join(base_dir,"lib/hmm_names")])
			else:
				os.system(" ".join([os.path.join(base_dir,"htk\\bin.win32\\HCopy.exe"), "-C", os.path.join(base_dir,"lib\\config.parming"), "-S", os.path.join(TMP,"audios.scp")]))
				#subprocess.run([os.path.join(base_dir,"htk\\bin.win32\\HCopy.exe"), "-C", os.path.join(base_dir,"lib\\config.parming"), "-S", "audios.scp"])
				if(hmmdefs):	
					subprocess.run([os.path.join(base_dir,"htk\\bin.win32\\HVite.exe"), "-a", "-C", \
							os.path.join(base_dir,"lib\\config"), "-H", os.path.join(base_dir,"models\\hmm\\hmmdefs"),\
							"-I", os.path.join(TMP,"mlf.mlf"), "-S", os.path.join(TMP,"mfc.matl"), "-i", \
							os.path.join(TMP,"recog.out"), os.path.join(TMP,"dict"), os.path.join(TMP,"hmm_names")])
				else:
					subprocess.run([os.path.join(base_dir,"htk\\bin.win32\\HVite.exe"), "-a", "-C", \
							os.path.join(base_dir,"lib\\config"), "-H", os.path.join(base_dir,"models\\hmm\\hmmdefs"), \
							"-I", os.path.join(TMP,"mlf.mlf"), "-S", os.path.join(TMP,"mfc.matl"), "-i", \
							os.path.join(TMP,"recog.out"), os.path.join(TMP,"dict"), os.path.join(base_dir,"lib\\hmm_names")])
				
		elif(aligner == 'Kaldi'):
			if('linux' in sys.platform.lower()):	
				subprocess.run(["cp", os.path.join(TMP,"train.lab"), os.path.join(base_dir,"corpus/train.lab")])
				command = [os.path.join(base_dir,"lib/align")]
				command.append("-t") 
				command.append(os.path.join(base_dir,"trash/"))
				if(config):
					command.append("--config_path")
					command.append("config.yaml")
				command.append(os.path.join(base_dir,"corpus/"))
			elif('darwin' in sys.platform.lower()):
				subprocess.run(["cp", os.path.join(TMP,"train.lab"), os.path.join(base_dir,"corpus/train.lab")])
				command = [os.path.join(base_dir,"mac/lib/align")]
				command.append("-t")
				command.append(os.path.join(base_dir,"trash/"))
				if(config):
					command.append("--config_path")
					command.append("config.yaml")
				command.append(os.path.join(base_dir,"corpus/"))
			else:
				os.system(" ".join(["move", os.path.join(TMP,"train.lab"), os.path.join(base_dir,"corpus\\train.lab")]))
				#subprocess.run(["move", "train.lab", os.path.join(base_dir,"corpus\\train.lab")])
				command = [os.path.join(base_dir,"win\\bin\\mfa_align.exe")]
				command.append("-t")
				command.append(os.path.join(base_dir,"trash\\"))
				if(config):
					command.append("--config_path")
					command.append("config.yaml")
				command.append(os.path.join(base_dir,"corpus\\"))

			command.append(os.path.join(TMP,"dict"))
			if(hmmdefs):
				command.append(os.path.join(TMP,"model.zip"))
			else:
				if('win' not in sys.platform.lower()):	
					command.append(os.path.join(base_dir,"models/pt.zip"))
					command.append("output/")
				else:
					command.append(os.path.join(base_dir,"models\\pt.zip"))
					command.append("output\\")
			
			#por algum motivo só executa certo com o os.system
			os.system(" ".join(command))			

			#subprocess.run(command)
	@staticmethod
	def format_output(text, filename, out_format, aligner='HTK'):
		tc = TextConverter()
		if(aligner == 'HTK'):
			if(out_format == 'palavra'):		
				tc.generate_textgrid(filename, repl=text)
			elif(out_format == 'todos'):
				tc.generate_textgrid(filename, mul_text=True)
			else:
				tc.generate_textgrid(filename)
		elif(aligner == 'Kaldi'):
			if('win' not in sys.platform.lower()):
				tc.textgrid_to_lab("output/corpus/train.TextGrid", os.path.join(TMP,"train.lab"))
			else:
				tc.textgrid_to_lab("output\\corpus\\train.TextGrid", os.path.join(TMP,"train.lab"))
			if(out_format=='todos'):
				tc.multi_split(os.path.join(TMP,"train.lab"), filename.replace(".wav",".TextGrid"), os.path.join(TMP,'text1.out'), os.path.join(TMP,'text2.out'))
			else:
				tc.lab_to_textgrid(os.path.join(TMP,"train.lab"), filename.replace(".wav", ".TextGrid"))
	
	def lab_to_textgrid(self, ifname, ofname):
		inf = open(ifname, 'r')
		outf = open(ofname, 'w')

		# get info from .lab
		labs = []
		for line in inf:
			if not re.search('^\s*\d+\s*\d+\s*\S+', line): #regular expresion for "space number space number space word"
				continue
			tokens = line.split()
			time = tokens[1].strip()
			label = tokens[2].strip()
			labs.append((str(int(time)/10000000.0), label))
		maxtime = str(labs[-1][0])

		# boilerplate
		outf.write('File type = "ooTextFile"\n')
		outf.write('Object class = "TextGrid"\n')
		outf.write('\n')
		outf.write('xmin = 0\n')
		outf.write('xmax = ' + maxtime + '\n')
		outf.write('tiers? <exists>\n')
		outf.write('size = 1\n')
		outf.write('item []:\n')
		outf.write('    item [1]:\n')
		outf.write('        class = "IntervalTier"\n')
		outf.write('        name = "labels"\n')
		outf.write('        xmin = 0\n')
		outf.write('        xmax = ' + maxtime + '\n')
		outf.write('        intervals: size = ' + str(len(labs)) + '\n')

		# intervals
		count = 0
		prevtime = '0'
		for elt in labs:
			count += 1
			outf.write('        intervals [' + str(count) + ']:\n')
			outf.write('            xmin = ' + prevtime + '\n')
			outf.write('            xmax = ' + elt[0] + '\n')
			outf.write('            text = "' + elt[1] + '"\n')
			prevtime = elt[0]

		inf.close()
		outf.close()

	def multi_split(self, ifname, ofname, name2, name3):
		inf = open(ifname, 'r')
		outf = open(ofname, 'w')

		with open(name2, "r") as f:
			syl = f.read().split()

		with open(name3, "r") as f:
			words = f.read().split()

		# get info from .lab
		labs = []
		for line in inf:
			if not re.search('^\s*\d+\s*\d+\s*\S+', line): #regular expresion for "space number space number space word"
				continue
			tokens = line.split()
			time = tokens[1].strip()
			label = tokens[2].strip()
			labs.append((str(int(time)/10000000.0), label))

		maxtime = str(labs[-1][0])
		
		# boilerplate
		outf.write('File type = "ooTextFile"\n')
		outf.write('Object class = "TextGrid"\n')
		outf.write('\n')
		outf.write('xmin = 0\n')
		outf.write('xmax = ' + maxtime + '\n')
		outf.write('tiers? <exists>\n')
		outf.write('size = 3\n')
		outf.write('item []:\n')
		outf.write('    item [1]:\n')
		outf.write('        class = "IntervalTier"\n')
		outf.write('        name = "labels"\n')
		outf.write('        xmin = 0\n')
		outf.write('        xmax = ' + maxtime + '\n')
		outf.write('        intervals: size = ' + str(len(labs)) + '\n')


		beg = []
		end = []
		let = []

		count = 0
		prevtime = '0'
		for elt in labs:
			count += 1
			outf.write('        intervals [' + str(count) + ']:\n')
			outf.write('            xmin = ' + prevtime + '\n')
			outf.write('            xmax = ' + elt[0] + '\n')
			outf.write('            text = "' + elt[1] + '"\n')
			beg.append(prevtime)
			end.append(elt[0])
			let.append(elt[1])
			prevtime = elt[0]

		n_sil = sum([1 if x=='sil' else 0 for x in let])

		outf.write('    item [2]:\n')
		outf.write('        class = "IntervalTier"\n')
		outf.write('        name = "labels"\n')
		outf.write('        xmin = 0\n')
		outf.write('        xmax = ' + maxtime + '\n')
		outf.write('        intervals: size = ' + str(len(syl)+n_sil) + '\n')

		count1 = 0
		count = 0
		prevtime = '0'
		b_time = '0'
		a = ''

		for pos, text in enumerate(let):
			a = a + text

			if(a == 'sil'):
				outf.write('        intervals [' + str(count+1) + ']:\n')
				outf.write('            xmin = ' + b_time + '\n')
				outf.write('            xmax = ' + end[pos] + '\n')
				outf.write('            text = "sil"\n')
				a = ''
				count += 1
				if(len(beg) > pos + 1):
					b_time = beg[pos+1]
			elif(a == syl[count1]):
				outf.write('        intervals [' + str(count+1) + ']:\n')
				outf.write('            xmin = ' + b_time + '\n')
				outf.write('            xmax = ' + end[pos] + '\n')
				outf.write('            text = "' + syl[count1] + '"\n')
				count += 1
				count1 += 1
				a = ''
				if(len(beg) > pos + 1):
					b_time = beg[pos+1]

		outf.write('    item [3]:\n')
		outf.write('        class = "IntervalTier"\n')
		outf.write('        name = "labels"\n')
		outf.write('        xmin = 0\n')
		outf.write('        xmax = ' + maxtime + '\n')
		outf.write('        intervals: size = ' + str(len(words)+n_sil) + '\n')

		count = 0
		count1 = 0
		prevtime = '0'
		b_time = '0'
		a = ''
		for pos, text in enumerate(let):
			a = a + text
			if(a == 'sil'):
				outf.write('        intervals [' + str(count+1) + ']:\n')
				outf.write('            xmin = ' + b_time + '\n')
				outf.write('            xmax = ' + end[pos] + '\n')
				outf.write('            text = "sil"\n')
				a = ''
				count += 1
				if(len(beg) > pos + 1):
					b_time = beg[pos+1]
			elif(a == words[count1]):
				outf.write('        intervals [' + str(count+1) + ']:\n')
				outf.write('            xmin = ' + b_time + '\n')
				outf.write('            xmax = ' + end[pos] + '\n')
				outf.write('            text = "' + words[count1] + '"\n')
				count += 1
				count1 += 1
				a = ''
				if(len(beg) > pos + 1):
					b_time = beg[pos+1]

		inf.close()
		outf.close()
	
	def textgrid_to_lab(self, ifname, ofname, aligner='HTK'):
		# boilerplate
		outf = open(ofname, 'w')

		# intervals
		inf = open(ifname)
		start_of_intervals = False
		start = ''
		end = ''
		text = ''
		f_short = False

		for line in inf:
			if('File type' in line):
				if("ooTextFile short" in line):
					f_short = True
				else:
					f_short = False
				break
		
		new_file = []
		already = False if aligner=='HTK' else True
		if(not f_short):
			for line in inf:
				l = line.strip()
				if(already and "item [2]:" in line):
					break
				if("item [2]:" in line):
					already=True
				if(already):
					if not start_of_intervals:
						if re.search('^intervals', l):
							start_of_intervals = True
						else:
							continue
					if re.search('^xmin', l):
						start = float(l.strip('xmin = '))
					elif re.search('^xmax', l):
						end = l.strip('xmax = ')
					elif re.search('^text', l):  # end of interval; write info
						text = l.strip('text = ').strip('"')
						if(text=='' or text=='sp'):
							new_file[-1] = " ".join([j if i!=1 else str(int(float(end)*10000000)) for i,j in enumerate(new_file[-1].split())])
						else:
							new_file.append('%d %d ' %(int(float(start)*10000000), int(float(end)*10000000)) + text)
					else:
						continue
			
			outf.write('\n'.join(new_file))
		else:
			count = 0
			beg=0
			end=0
			for line in inf:
				if('<exists>' in line):
					count+=1
				if(count >= 8):
					if(isFloat(line.strip())):
						beg = end
						end = float(line.strip())
					else:
						text = line.strip('"')
						if(text==''):
							text='sil' 
						outf.write('\t%.5f %.5f ' %(float(beg), float(end)) + text + '\n')
				else:
					count += 1	
		outf.close()
		inf.close()
