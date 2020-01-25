from dataclasses import dataclass

from thirdparty.purlovia.ue.stream import MemoryStream

@dataclass
class UE4OpusHeader(object):
	StartOffset: int
	SampleRate: int
	SampleNum: int
	ChannelCount: int
	DataSize: int
	Version: int

def guess_version(stream: MemoryStream, offset) -> int:
	return 1

def read_header(stream: MemoryStream) -> UE4OpusHeader:
	start_offset = 0x11
	sample_rate = stream.readUInt16()
	num_samples = stream.readUInt32()
	channel_count = stream.readUInt8()
	data_size = len(stream) - start_offset
	version = guess_version(stream, start_offset)
	return UE4OpusHeader(
		StartOffset=start_offset,
		SampleRate=sample_rate,
		SampleNum=num_samples,
		ChannelCount=channel_count,
		DataSize=data_size,
		Version=version,
	)
