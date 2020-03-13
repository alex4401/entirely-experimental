import os
import sys
import struct
from pathlib import Path
from Purlovia_stream import MemoryStream

def read_asset_guid(fp):
	stream = MemoryStream(fp.read())
	stream.offset += 4 * 5 + 4 + 4
	stream.offset += stream.readUInt32()
	stream.offset += 4 + 4 * 2 * 4 + 4 + 4 + 4
	return [stream.readUInt32() for _ in range(4)]

tree_path = Path('./tree')
uassets = list(tree_path.glob('**/*.uasset'))

size = len(uassets)

_offset = 0
def pack(fmt, buf, *args):
	global _offset
	p = struct.pack(fmt, *args)
	_offset += len(p)
	buf.write(p)

with open(sys.argv[1], 'wb') as fp:
	pack('<I', fp, size)

	for uasset in uassets:
		orig = uasset
		uasset = ('/Game' + str(uasset)[4:-7]).upper()
		print(f'Processing {uasset}')

		with open(orig, 'rb') as fp2:
			guid = read_asset_guid(fp2)

		pack('<I', fp, len(uasset) + 1)
		for c in uasset:
			pack('c', fp, c.encode('ascii'))
		pack('c', fp, bytes([0]))
		pack('<IIII', fp, *guid)
		pack('<I', fp, os.stat(orig).st_size)
		pack('<I', fp, 0)
