import sys
from Purlovia_stream import MemoryStream

with open(sys.argv[1], 'rb') as fp:
	stream = MemoryStream(fp.read())
	size = stream.readUInt32()
	print('Size:', size)

	for _ in range(size):
		strlen = stream.readUInt32()
		str = stream.readTerminatedString(strlen)
		unk1 = stream.readUInt32()
		unk2 = stream.readUInt32()
		unk3 = stream.readUInt32()
		unk4 = stream.readUInt32()
		fsize = stream.readUInt32()
		unk6 = stream.readUInt32()
		if str.lower().startswith(sys.argv[2].lower()):
			print(str)
			print(f'unk1 = {hex(unk1)}')
			print(f'unk2 = {hex(unk2)}')
			print(f'unk3 = {hex(unk3)}')
			print(f'unk4 = {hex(unk4)}')
			print(f'fsize = {fsize}')
			print(f'unk6 = {hex(unk6)}')
	if len(stream) != stream.offset:
		print('Remaining bytes: {len(stream) - stream.offset}')
