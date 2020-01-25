from thirdparty.purlovia.ue.stream import MemoryStream

from head import UE4OpusHeader

def stream__jump(stream: MemoryStream, offset: int):
	if not hasattr(stream, 'saved_offsets'):
		stream.saved_offsets = []

	stream.saved_offsets.append(stream.offset)
	stream.offset = offset

def stream__revert_jump(stream: MemoryStream):
	stream.offset = stream.saved_offsets.pop()
