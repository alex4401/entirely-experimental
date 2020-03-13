import os
import sys
import struct
from pathlib import Path
from Purlovia_stream import MemoryStream

_offset = 0
def pack(fmt, buf, *args):
	global _offset
	p = struct.pack(fmt, *args)
	_offset += len(p)
	buf.write(p)

with open(sys.argv[1], 'rb') as fp1:
	with open(sys.argv[2], 'rb') as fp2:
		with open(sys.argv[3], 'wb') as fp_w:
			stream1 = MemoryStream(fp1.read())
			stream2 = MemoryStream(fp2.read())
			size1 = stream1.readUInt32()
			size2 = stream2.readUInt32()
			print(f'len(In1) = {size1}, len(In2) = {size2}')
			size = size1 + size2
			
			pack('<I', fp_w, size)

			o1 = len(stream1) - 4
			o2 = len(stream2) - 4
			print(f'Remaining bytes in: In1={o1}, In2={o2}')
			fp_w.write(stream1.readBytes(o1))
			fp_w.write(stream2.readBytes(o2))
