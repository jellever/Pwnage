import string
import itertools
import random

#Python implementation of reverse CRC algo in http://www.danielvik.com/2010/10/calculating-reverse-crc.html


#Custom CRC table, replace with your own
table = []

import ctypes
import string


def crc32(crc, data):
	for i in range(len(data)):
		result =  (crc ^ ord(data[i]))
		resultByte = ctypes.c_byte(result).value
		crc = (crc >> 8) ^ table[resultByte]
	return ~crc


def FindReverseCRC32(data, expectedCrc):
	beginCrc = crc32(0, data)
	tableIdx = [0,0,0,0]
	patchBytes = [0,0,0,0]
	iterCrc = ~expectedCrc
	for j in xrange(3, -1, -1):
		for i in xrange(0, 256):
			if (((iterCrc ^ table[i]) >> 24) == 0):
				tableIdx[j] = i
				iterCrc = (iterCrc ^ table[i]) << 8				
				break

	crc = ~beginCrc
	for j in xrange(0, 4):
		patchBytes[j] = (crc ^ tableIdx[j]) & 0xff
		crc = (crc >> 8) ^ table[patchBytes[j] ^ (crc & 0xff)]		
	
	patchChars = []
	for patchByte in patchBytes:
		patchChars.append(chr(patchByte))

	return patchChars

def FindReverseCRC32Str(data, expectedCrc):
	patchChars = FindReverseCRC32(data, expectedCrc)
	return ''.join(patchChars)

if __name__ == '__main__':
	toMatchCrc = 0xDEADBEEF
	inp = ''.join(random.choice(string.lowercase) for i in range(12))

	print "Input: {}".format(inp)
	print 'To match CRC: 0x{:x}'.format(toMatchCrc)
	patchStr =  FindReverseCRC32Str(inp, toMatchCrc)
	finalstr = (inp + patchStr).encode('string_escape')
	print '\n4 patch bytes: {}'.format(patchStr.encode('string_escape'))
	print 'Final string matching crc "0x{:x}": {}'.format(toMatchCrc, finalstr)

