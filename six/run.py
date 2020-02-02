import sys
import json

import numpy

from math import floor
from typing import Tuple
from PIL import Image
from tuples import Color3, Color4, ChannelConfig
from gamma import from_linear_pixelf, from_linear_color
from fmath import lerp, choose_darker, to_pixelf, to_pixeli, clamp_pixel, sum_pixels, mul_pixelf

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
final = Image.new('RGB', target_size)

# Generate channel masks
def get_single_channel_cmy(texture: Image, decisive_channels: Tuple[int, int]) -> Image:
	output = Image.new('L', target_size)
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = texture.getpixel((x, y))
			#pixel_in = from_linear_pixelf(pixel_in)
			pixel_cmp1 = [pixel_in[index] if index == decisive_channels[0] else 0 for index in range(3)]
			pixel_cmp2 = [pixel_in[index] if index == decisive_channels[1] else 0 for index in range(3)]
			#pixel_cmp1 = to_pixeli(pixel_cmp1)
			#pixel_cmp2 = to_pixeli(pixel_cmp2)
			pixel_out = choose_darker(pixel_cmp1, pixel_cmp2)
			output.putpixel((x, y), sum(pixel_out))
	return output

m_red, m_green, m_blue = mask.split()
m_cyan = get_single_channel_cmy(mask, (0, 1)) # sic
m_yellow = get_single_channel_cmy(mask, (1, 2)) # sic
m_magenta = get_single_channel_cmy(mask, (0, 2))

# Colorise the texture
def colorise(source: Image, target: Image, info: ChannelConfig):
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = source.getpixel((x, y))
			L = pixel_in / 255#from_linear_color(pixel_in / 255)

			pixel_out = info.target#from_linear_pixelf(info.target)
			pixel_out = mul_pixelf(pixel_out, info.intensity)
			pixel_out = mul_pixelf(pixel_out, L)

			pixel_out = to_pixeli(pixel_out)
			pixel_out = sum_pixels(target.getpixel((x, y)), pixel_out)
			pixel_out = clamp_pixel(0, pixel_out, 255)
			target.putpixel((x, y), pixel_out)

colorise(m_red, colorised, ChannelConfig(**configs['red']))
colorise(m_green, colorised, ChannelConfig(**configs['green']))
colorise(m_blue, colorised, ChannelConfig(**configs['blue']))
colorise(m_cyan, colorised, ChannelConfig(**configs['cyan']))
colorise(m_yellow, colorised, ChannelConfig(**configs['yellow']))
colorise(m_magenta, colorised, ChannelConfig(**configs['magenta']))

# Blend colorisation with diffuse
for x in range(target_size[0]):
	for y in range(target_size[1]):
		a = diffuse.getpixel((x, y))
		b = colorised.getpixel((x, y))
		pixel_out = (floor(a[0] / 255 * b[0]), floor(a[1] / 255 * b[1]), floor(a[2] / 255 * b[2]))
		colorised.putpixel((x, y), pixel_out)

# Save
colorised.save('out.png')
