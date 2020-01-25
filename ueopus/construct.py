import sys
from dataclasses import dataclass
from typing import List

from thirdparty.purlovia.ue.stream import MemoryStream
from head import UE4OpusHeader

@dataclass
class OpusMetadata(object):
	Vendor: str
	Comment: str

def _pack_str(data: str, length: int) -> List[int]:
	buf = []
	buf += length.to_bytes(4, byteorder='little', signed=False)
	for char in data:
		buf.append(ord(char))
	return buf

def construct_opus_head(uo_header: UE4OpusHeader, skip: int) -> List[int]:
	buf = []

	mapping_family = 0
	if uo_header.ChannelCount > 2:
		mapping_family = 1

	buf += 0x4F707573.to_bytes(4, byteorder='big', signed=False) # Opus
	buf += 0x48656164.to_bytes(4, byteorder='big', signed=False) # Head
	buf.append(1) # Version
	buf.append(uo_header.ChannelCount)
	buf += int(skip).to_bytes(2, byteorder='little', signed=False)
	buf += uo_header.SampleRate.to_bytes(4, byteorder='little', signed=False)
	buf += int(0).to_bytes(4, byteorder='little', signed=False)
	buf.append(0)

	if mapping_family > 0:
		print('Mapping family is different from 0. Not implemented.')
		sys.exit(1)

	return buf

def construct_opus_comment(meta: OpusMetadata) -> List[int]:
	buf = []
	m_vendor_len = len(meta.Vendor)
	m_comment_len = len(meta.Comment)
	comment_size = 0x14 + m_vendor_len + m_comment_len
	
	buf += 0x4F707573.to_bytes(4, byteorder='big', signed=False) # Opus
	buf += 0x54616773.to_bytes(4, byteorder='big', signed=False) # Tags
	buf += _pack_str(meta.Vendor, m_vendor_len)
	buf += int(1).to_bytes(4, byteorder='little', signed=False)
	buf += _pack_str(meta.Comment, m_comment_len)

	return buf

