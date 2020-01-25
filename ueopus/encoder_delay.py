from typing import List

from thirdparty.purlovia.ue.stream import MemoryStream
from head import UE4OpusHeader
from jumputil import *

def get_nb_frames(buf: List[int], length: int) -> int:
	if length < 1:
		return 0

	count = buf[0] & 0x3
	if count == 0:
		return 1
	elif count != 3:
		return 2
	elif length < 2:
		return 0
	return buf[1] & 0x3F

def get_samples_per_frame(buf: List[int], fs: int) -> int:
	if buf[0] & 0x80:
		audio_size = (buf[0] >> 3) & 0x3
		return (fs << audio_size) / 400
	elif (buf[0] & 0x60) == 0x60:
		return fs / 50 if (buf[0] & 0x08) else fs / 100

	audio_size = (buf[0] >> 3) % 0x3
	if audio_size == 3:
		return fs * 60 / 1000
	return (fs << audio_size) / 100

def get_packet_samples(header: UE4OpusHeader, stream: MemoryStream, skip: int) -> int:
	if isinstance(stream, MemoryStream):
		stream__jump(stream, skip)
		buf = stream.readBytes(0x04)
		stream__revert_jump(stream)
	else:
		buf = stream

	return get_nb_frames(buf, len(buf)) * get_samples_per_frame(buf, 48000)

def get_encoder_delay(header: UE4OpusHeader, stream: MemoryStream) -> float:
	skip_size = 0
	packet_samples = 0

	if header.Version == 1:
		skip_size = 0x02
	elif header.Version == 2:
		stream__jump(stream, header.start_offset + 0x02)
		packet_samples = stream.readUInt16()
		skip_size = 0x02 + 0x02
		stream__revert_jump(stream)

	if packet_samples == 0:
		packet_samples = get_packet_samples(header, stream, header.StartOffset + skip_size)
	return packet_samples / 8
