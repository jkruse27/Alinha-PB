from sly import Lexer, Parser

class PhonemeLexer(Lexer):
	tokens = {MAI,MIN,TON,PAR,S_CONS,CONS,SPACE,END,SIL}

	SIL = r'sil'
	PAR = r'([aiueoAIUEO],*[IU])|([aiueoAIUEO],*hU)|([ao],*NI)|([aA],*NU)|([UI][IAU])'
	TON = r'([aiueo],[Nh])|([eo],hI)|([aiueo],)'
	MAI = r'([AIUEO]N)|([AIUEO])'
	MIN = r'([aiueo]h)|([eo]hI)|([aiueo]N)|([aiueo])'
	S_CONS = r'^(zh|nh|tS|sh|dZ|lh|[ptksbdgfvzSZmnrNRl])'
	CONS = r'zh|nh|tS|sh|dZ|lh|[ptksbdgfvzSZmnrNRl]'
	SPACE = r'\ '
	END = r'<<EOF>>|\n'
 
	def error(self, t):
		self.index += 1


class PhonemeParser(Parser):
	tokens = PhonemeLexer.tokens

	@_('FRASE VOGAL END')
	def FRASE(self, p):
		return " ".join(p).replace(',','').strip()

	@_('FRASE VOGAL')
	def FRASE(self, p):
		return " ".join(p).replace(',','').strip()
	@_('SIL')
	def FRASE(self, p):
		return p

	@_('empty')
	def FRASE(self, p):
		return ''

	@_('MAI MIN')
	def VOGAL(self, p):
		return "".join(p)

	@_('MAI SPACE MIN')
	def VOGAL(self, p):
		return p[0]+p[2]

	@_('MIN SPACE MIN')
	def VOGAL(self, p):
		return p[0]+p[2]

	@_('MAI SPACE MAI')
	def VOGAL(self, p):
		return p[0]+p[2]

	@_('TON SPACE')
	def VOGAL(self, p):
		return p[0]

	@_('PAR SPACE')
	def VOGAL(self, p):
		return p[0]

	@_('MIN SPACE')
	def VOGAL(self, p):
		return p[0]

	@_('MAI SPACE')
	def VOGAL(self, p):
		return p[0]

	@_('VOGAL SPACE CONSOANTE')
	def VOGAL(self, p):
		return p[0]+p[2]

	@_('MAI TON MAI')
	def VOGAL(self, p):
		return "".join(p)

	@_('MAI TON')
	def VOGAL(self, p):
		return "".join(p)

	@_('MIN MIN')
	def VOGAL(self, p):
		return "".join(p)

	@_('PAR')
	def VOGAL(self, p):
		return p[0]

	@_('MAI MAI')
	def VOGAL(self, p):
		return p[0]

	@_('TON')
	def VOGAL(self, p):
		return p[0]

	@_('MIN')
	def VOGAL(self, p):
		return p[0]

	@_('MAI')
	def VOGAL(self, p):
		return p[0]

	@_('VOGAL CONSOANTE')
	def VOGAL(self, p):
		return "".join(p)

	@_('S_CONS')
	def VOGAL(self, p):
		return p[0]

	@_('CONS CONSOANTE')
	def CONSOANTE(self, p):
		return "".join(p)

	@_('CONS SPACE')
	def CONSOANTE(self, p):
		return p[0]

	@_('CONS')
	def CONSOANTE(self, p):
		return p[0]

	@_('')
	def empty(self, p):
		pass

