#!/usr/bin/env python
from hash_map import *
import sys
import os
import subprocess
from flask import Flask, send_file, jsonify, session, redirect, url_for,request, render_template
from TextConverter import *
from Conversor import *
import random, time
import subprocess
import wave
import contextlib

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
	base_dir = os.path.join(sys._MEIPASS)

TMP = os.path.join(base_dir,'tmp/')

def clean_tg():
	if('win' not in sys.platform.lower()):
		subprocess.run(['rm','-f', '*.TextGrid'])
		subprocess.run(['rm','-f','-r','output'])
	else:
		os.system(" ".join(['del', '*.TextGrid', '>NUL 2>&1']))
		#subprocess.run(['del',\
		#		'*.wav',\
		#		'a',\
		#		'b',\
		#		'*.mlf',\
		#		'dict',\
		#		'*.out',\
		#		'*.lab',\
		#		'*.scp',\
		#		'*.matl',\
		#		'*.mfc',\
		#		'hmmdefs',\
		#		'*.TextGrid'],\
		#		stdout=subprocess.DEVNULL,\
		#		stderr=subprocess.DEVNULL)


def clean():
	if('win' not in sys.platform.lower()):
		subprocess.run(['rm',\
				'-f',\
				os.path.join(TMP,'*.wav'),\
				os.path.join(TMP,'a'),\
				os.path.join(TMP,'b'),\
				os.path.join(TMP,'dict'),\
				os.path.join(TMP,'*.mlf'),\
				os.path.join(TMP,'*.out'),\
				os.path.join(TMP,'*.lab'),\
				os.path.join(TMP,'*.scp'),\
				os.path.join(TMP,'*.matl'),\
				os.path.join(TMP,'*.mfc'),\
				os.path.join(TMP,'hmmdefs')])
		subprocess.run(['rm','-f','-r','output'])
	else:
		os.system(" ".join(['del',\
				os.path.join(TMP,'*.wav'),\
				os.path.join(TMP,'a'),\
				os.path.join(TMP,'b'),\
				os.path.join(TMP,'*.mlf'),\
				os.path.join(TMP,'dict'),\
				os.path.join(TMP,'*.out'),\
				os.path.join(TMP,'*.lab'),\
				os.path.join(TMP,'*.scp'),\
				os.path.join(TMP,'*.matl'),\
				os.path.join(TMP,'*.mfc'),\
				os.path.join(TMP,'hmmdefs'),\
				'>NUL 2>&1']))
		#subprocess.run(['del',\
		#		'*.wav',\
		#		'a',\
		#		'b',\
		#		'*.mlf',\
		#		'dict',\
		#		'*.out',\
		#		'*.lab',\
		#		'*.scp',\
		#		'*.matl',\
		#		'*.mfc',\
		#		'hmmdefs',\
		#		'*.TextGrid'],\
		#		stdout=subprocess.DEVNULL,\
		#		stderr=subprocess.DEVNULL)


app = Flask(__name__,
        static_folder=os.path.join(base_dir, 'static'),
        template_folder=os.path.join(base_dir, 'templates'))

#app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = TMP
app.config['MAX_CONTENT_PATH'] = 1000000000

@app.route('/')
@app.route('/index')
def index():
	clean_tg()
	return render_template('index.html', convertion='')

@app.route('/about')
def about():
	return render_template('about.html', convertion='')

@app.route('/how')
def how():
	return render_template('how.html', convertion='')

@app.route('/align')
def align():
	return render_template('alinhador.html', convertion='')

@app.route('/kaldi')
def kaldi():
	return render_template('kaldi.html', convertion='')

@app.route('/meta')
def meta():
	return render_template('meta.html', convertion='')

@app.route('/submit', methods=['POST'])
def submit():
	try:
		converter = Conversor()
		convertion = converter.convert_sentence(request.form['text'])
		return render_template('index.html', convertion=convertion)
	except Exception as e:
		return "Ocorreu um erro!\n" + str(e) + "\n Verifique a página sobre para mais informações sobre possíveis erros\n"

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	try:
		if request.method == 'POST':
			clean_tg()
			# Recebendo arquivos e entradas			

			f = request.files['file']
			filename = f.filename
			filename = os.path.join(TMP, filename)
			f.save(filename)

			text=request.form['text']
			
			hmmdefs = False
			if (request.files['hmm'].filename != ''):
				g = request.files['hmm']
				g.save(os.path.join(TMP, "hmmdefs"))
				hmmdefs = True

			req_in = request.form['in']
			req_out = request.form['options']
			aligner='HTK'

			# Cria todos os arquivos necessarios para o alinhamento	
			text1 = TextConverter.perform_conversion(text, 
								 filename,
								 req_in,
								 req_out,
								 aligner=aligner)

			TextConverter.align(text, filename, req_in, req_out, hmmdefs=hmmdefs, aligner=aligner)

			# Formata o arquivo de saida para o formato desejado
			TextConverter.format_output(text1, filename, req_out, aligner=aligner)
			clean()
			return redirect("/download/%s" %(filename[len(TMP):]))

	except Exception as e:
		return "Ocorreu um erro!\n" + str(e) + "\n Verifique a página sobre para mais informações sobre possíveis erros\n"
	
@app.route('/uploader_kaldi', methods = ['GET', 'POST'])
def uploader_kaldi():
	try:
		if request.method == 'POST':
			clean_tg()

			# Recebendo arquivos
			f = request.files['file']
			filename = f.filename
			filename = os.path.join(TMP, filename)
			f.save(filename)

			text=request.form['text']
			
			model = False
			if (request.files['model'].filename != ''):
				g = request.files['model']
				g.save(os.path.join(TMP,"model.zip"))
				model = True
			config = False
			if (request.files['config'].filename != ''):
				g = request.files['config']
				g.save(os.path.join(TMP,"config.yaml"))
				config = True
			
			if('win' not in sys.platform):
				subprocess.run(["rm", "-f", "corpus/*"])
				subprocess.run(["cp", filename, "corpus/train.wav"])
			else:
				os.system(" ".join(["del", "/s","/q","corpus\\*", ">NUL 1>&2"]))
				#subprocess.run(["del", "/s", "/q", "corpus\\*"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
				os.system(" ".join(["move", filename, os.path.join(base_dir,"corpus\\train.wav")]))
				#subprocess.run(["move", filename, os.path.join(base_dir,"corpus\\train.wav")])	

			aligner = 'Kaldi'
			req_in = request.form['in']
			req_out = request.form['options']

			# Cria todos os arquivos necessarios para o alinhamento	
			text1 = TextConverter.perform_conversion(text, 
							 filename,
							 req_in,
							 req_out,
							 aligner=aligner)

			TextConverter.align(text, filename, req_in, req_out, hmmdefs=model, aligner=aligner,config=config)
			
			# Formata o arquivo de saida para o formato desejado
			TextConverter.format_output(text1, filename, req_out, aligner=aligner)
			clean()
			return redirect("/download/%s" %(filename[len(TMP):]))
	except Exception as e:
		return "Ocorreu um erro!\n" + str(e) + "\n Verifique a página sobre para mais informações sobre possíveis erros\n"

@app.route('/download/<name>', methods=['GET', 'POST'])
def download(name):
	path = os.path.join(TMP,name.replace("wav", "TextGrid"))
	return send_file(path, as_attachment=True)

		
@app.route('/add', methods=['GET', 'POST'])
def add():
	base_dir = '.'
	if hasattr(sys, '_MEIPASS'):
		base_dir = os.path.join(sys._MEIPASS)
        
	a = ExceptionHashMap(os.path.join(base_dir,"Dictionaries/Exceptions.json"))
	a.create_hash()
	if(request.form["button"]=="add"):
		try:
			text=request.form['text'].split()
			pho=request.form['phoneme'].split()
			for i, j in enumerate(text):
				a.add_exception(j.lower(), pho[i], 'simple')
		except Exception as e:
			return "Ocorreu um erro!\n" + str(e) + "\n Verifique a página sobre para mais informações sobre possíveis erros\n"
	elif(request.form["button"]=="rem"):
		try:
			text=request.form['text'].split()
			for i in text:
				a.remove_exception(i.lower(), 'simple')
		except Exception as e:
			return "Ocorreu um erro!\n" + str(e) + "\n Verifique a página sobre para mais informações sobre possíveis erros\n"
	dic, _ = a.getDictionary()  
	words = [i+": "+dic[i] for i in dic]
	a.store_hash()
	return render_template('add.html', lista=words)

@app.route('/ex')
def ex():
	a = ExceptionHashMap(os.path.join(base_dir, "Dictionaries/Exceptions.json"))
	a.create_hash()
	dic, _ = a.getDictionary()  
	words = [i+": "+dic[i] for i in dic]
	a.store_hash()
	return render_template('add.html', lista=words)

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
#app.run(host='127.0.0.1', port=port)
