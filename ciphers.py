import string
import re
import random
from unidecode import unidecode

class PolybiusSquare:
	def __init__(self, width=0, height=0, cipher=None, ij=True):
		if not ((width and height) or cipher):
			raise ValueError('Either choose the size of the square (width/height) or the encrypted cypher.')

		if cipher:
			cipher = cipher.lower()
			match = re.search(r'(\d+)x(\d+)#(?:\d+-\d+;?)+', cipher)
			if not match:
				raise ValueError('Can\'t find square size within the cipher, please specify with width and height parameters')

		self.width = width if width else int(match.group(1))
		self.height = height if height else int(match.group(2))

		self.abc = string.ascii_uppercase
		self.abc = self.abc.replace('J', '') if ij else self.abc

		if width * height < len(self.abc):
			raise ValueError('This square is not large enough to comprehend the whole alphabet.\nPlease increase width or height.')

		self.mount_square()

		if cipher:
			print(self.decrypt(match.group(0)))

	def mount_square(self):
		self.square_area = self.width * self.height
		self.abc_square = (self.abc * (self.square_area // len(self.abc) + 1))[:self.square_area]
		self.square = [self.abc_square[i:i+self.width] for i in range(0, len(self.abc_square), self.width)]

		self.abc_to_pos = {letter:[] for letter in self.abc}
		for line_index, line in enumerate(self.square):
			for col_index, letter in enumerate(line):
				self.abc_to_pos[letter].append('{}-{}'.format(col_index + 1, line_index + 1))
		
		self.pos_to_abc = {}
		for letter in self.abc:
			for pos in self.abc_to_pos[letter]:
				self.pos_to_abc[pos] = letter
		self.pos_to_abc['0-0'] = '�'

	def encrypt(self, text):
		text = unidecode(text).upper()
		text = text.replace('J', 'I') if len(self.abc) == 25 else text
		cipher = '{}x{}#'.format(self.width, self.height)
		positions = [random.choice(self.abc_to_pos.get(letter, ['0-0'])) for letter in text]
		cipher += ';'.join(positions)
		return cipher

	def decrypt(self, cipher):
		cipher = cipher.lower()
		match = re.search(r'(?:\d+x\d+#)?((?:\d+-\d+;?)+)', cipher)
		if match:
			positions = match.group(1).split(';')
			text = ''.join([self.pos_to_abc.get(pos, '0-0') for pos in positions])
			return text
		else:
			raise ValueError('Cipher doesn\'t match the Polybius Square pattern.')