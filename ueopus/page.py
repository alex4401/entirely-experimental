import struct
from typing import List

from thirdparty.purlovia.ue.stream import MemoryStream
from head import UE4OpusHeader
from jumputil import *
from checksum import get_oggs_checksum

_bitswap = ''.join([chr(sum([((val >> i) & 1) << (7-i) for i in range(8)]))
                       for val in range(256)])

def make_oggs_page(data: List[int], index: int, granule: int) -> List[int]:
	buf = []
	type_flag = 2 if index == 0 else 0
	serial_number = 0x7667
	segment_count = int(len(data) / 0xFF + 1)

	buf += 0x4F676753.to_bytes(4, byteorder='big', signed=False) # OggS
	buf.append(0) # Version
	buf.append(type_flag)
	buf += (granule >> 0 & 0xFFFFFFFF).to_bytes(4, byteorder='little', signed=False)
	buf += (granule >> 32 & 0xFFFFFFFF).to_bytes(4, byteorder='little', signed=False)
	buf += serial_number.to_bytes(4, byteorder='little', signed=False)
	buf += index.to_bytes(4, byteorder='little', signed=False)
	_checksum_offset = len(buf)
	buf += int(0).to_bytes(4, byteorder='little', signed=False) # Checksum placeholder
	buf.append(segment_count)

	lacing_done = 0
	i = 0
	while lacing_done < len(data):
		bytes_ = len(data) - lacing_done
		if bytes_ > 0xFF:
			bytes_ = 0xFF

		buf.append(bytes_)
		lacing_done += bytes_

		if lacing_done == len(data) and bytes_ == 0xFF:
			buf.append(0x00)
		i = i + 1
	buf += data

	crc = get_oggs_checksum(bytes(buf)) + 2**32
	crc_buf = crc.to_bytes(4, byteorder='little', signed=False)
	for index in range(0, 4):
		buf[_checksum_offset + index] = crc_buf[index]

	return buf
