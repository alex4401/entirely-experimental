import sys
import json

from typing import Tuple
from PIL import Image
from tuples import Color3, Color4, ChannelConfig
from gamma import from_linear_color
from fmath import lerp, choose_darker

if len(sys.argv) < 2:
	print('Usage: six mask diffuse config')
	sys.exit(1)

mask_filename = sys.argv[1]
diffuse_filename = sys.argv[2]
config_filename = sys.argv[3]

# Load textures
with open(config_filename, 'r') as config:
	configs = json.load(config)
diffuse = Image.open(diffuse_filename)
mask = Image.open(mask_filename)

assert diffuse.size == mask.size
target_size = mask.size

# Initialize new textures
colorised = Image.new('RGB', target_size)

# Generate channel masks
def get_single_channel_cmy(texture: Image, decisive_channels: Tuple[int, int]) -> Image:
	output = Image.new('L', target_size)
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = texture.getpixel((x, y))
			pixel_out = min(pixel_in[decisive_channels[0]], pixel_in[decisive_channels[1]])
			output.putpixel((x, y), (pixel_out, ))
	return output

m_red, m_green, m_blue = mask.split()
m_cyan = get_single_channel_cmy(mask, (0, 1)) # sic
m_yellow = get_single_channel_cmy(mask, (1, 2)) # sic
m_magenta = get_single_channel_cmy(mask, (0, 2))
