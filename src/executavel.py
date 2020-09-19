import pyinstaller.__main__

PyInstaller.__main__.run([
	'server.py',
	'-w',
	'-F',
	'--add-data="Dictionaries;Dictionaries"',
	'--add-data="htk;htk"',
	'--add-data="templates;templates"',
	'--add-data="static;static"',
	'--add-data="lib;lib"',
	'--add-data="models;models"',
	'--add-data="bin;bin"',
	'--add-data="corpus;corpus"',
	'--add-data="output;output"', 
	'--add-data="trash;trash"',
	'--add-data="win;win"'
])