import sys

def DumpBuffer(buf, length, caption="", dest=sys.stdout):
	def GetPrintableChar(str):
		if str.isalpha():
			return str
		else:
			return '.'

	print('---------> %s <--------- (%d bytes)\n' % (caption, length))
	print('       +0          +4          +8          +c           0   4   8   c\n')
	i = 0
	while i < length:
		if length - i > 16:
			l = 16
		else:
			l = length - i

		print('+%04x  ' % i)
		s = ' '.join(["%02x" % ord(c) for c in buf[i:i + l]])
		print(s)
		sp = 49 - len(s)
		print(' ' * sp)
		s = ''.join(["%c" % GetPrintableChar(c) for c in buf[i:i + l]])
		print(s)
		print('\n')

		i = i + 16
