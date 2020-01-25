import sys

from thirdparty.purlovia.ue.stream import MemoryStream
from head import read_header
from encoder_delay import get_encoder_delay, get_packet_samples
from construct import OpusMetadata, construct_opus_head, construct_opus_comment
from page import make_oggs_page

def from_file(filename: str) -> MemoryStream:
    fp = open(filename, "rb")
    data = fp.read()
    mem = memoryview(data)

    return MemoryStream(mem)

if len(sys.argv) < 2:
	print('Usage: ueopus input_file')
	sys.exit(1)

filename = sys.argv[1]
stream = from_file(filename)

# Check magic
if stream.readUInt32() != 0x4F344555: # UE4O
	print('Magic mismatch.')
	sys.exit(1)
stream.offset += 4

# Read
uo_header = read_header(stream)
print(uo_header)

encoder_delay = get_encoder_delay(uo_header, stream)
print('\tEncoder delay =', encoder_delay)

# Make head buffers
metadata = OpusMetadata(
	Vendor='Experiment',
	Comment='Repacked from Unreal\'s container format.',
)
head_buf = construct_opus_head(uo_header, encoder_delay)
comment_buf = construct_opus_comment(metadata)

# Pack into pages
head_page = make_oggs_page(head_buf, 0, 0)
comment_page = make_oggs_page(comment_buf, 1, 0)

with open('out.ogg', 'wb') as fp:
	fp.write(bytes(head_page))
	fp.write(bytes(comment_page))

	stream.offset = uo_header.StartOffset

	index = 2
	samples = 0
	while stream.offset < len(stream) - 1:
		size = stream.readUInt16()
		packet = stream.readBytes(size)
		samples += get_packet_samples(uo_header, packet, -1)
		fp.write(bytes(make_oggs_page(packet, index, int(samples))))
		index = index + 1
	#fp.write(stream.readBytes(len(stream) - stream.offset))
