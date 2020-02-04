import sys
import json

import numpy

from math import floor
from typing import Tuple
from PIL import Image
from tuples import Color3, Color4, ChannelConfig
from fmath import *

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
final = Image.new('RGBA', target_size)

# Generate channel masks
def get_single_channel_cmy(texture: Image, decisive_channels: Tuple[int, int]):
	output = dict()
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = texture.getpixel((x, y))
			pixel_in = int3_to_float3(pixel_in)
			pixel_in = float3_lin_to_srgb(pixel_in)
			pixel_out = min(pixel_in[decisive_channels[0]], pixel_in[decisive_channels[1]])
			output[(x, y)] = pixel_out
	return output

def convert_rgb(texture: Image):
	output = dict()
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = texture.getpixel((x, y))
			output[(x, y)] = pixel_in / 255
	return output

def sub12(a: dict, b: dict):
	output = dict()
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			v1 = a[(x, y)]
			v2 = b[(x, y)]
			output[(x, y)] = float1_clamp(0, v1 - v2, 256)
	return output

m_red, m_green, m_blue = mask.split()
rm_red = convert_rgb(m_red)
rm_green = convert_rgb(m_green)
rm_blue = convert_rgb(m_blue)

m_red = sub12(rm_red, rm_green)
m_red = sub12(m_red, rm_blue)
m_green = sub12(rm_green, rm_red)
m_green = sub12(m_green, rm_blue)
m_blue = sub12(rm_blue, rm_red)
m_blue = sub12(m_blue, rm_green)
m_cyan = get_single_channel_cmy(mask, (0, 1)) # sic
m_yellow = get_single_channel_cmy(mask, (1, 2)) # sic
m_magenta = get_single_channel_cmy(mask, (0, 2))

# Colorise the texture
def colorise(source: Image, target: dict, info: ChannelConfig):
	for x in range(target_size[0]):
		for y in range(target_size[1]):
			pixel_in = source[(x, y)]

			pixel_out = float3_lin_to_srgb(info.target)
			pixel_out = float3_mul_float1(pixel_out, info.intensity)
			pixel_out = float3_mul_float1(pixel_out, pixel_in)

			pixel_in = target.get((x, y), (0, 0, 0))
			target[(x, y)] = float3_add_float3(pixel_in, pixel_out)
temp = dict()
colorise(m_red, temp, ChannelConfig(**configs['red']))
colorise(m_green, temp, ChannelConfig(**configs['green']))
colorise(m_blue, temp, ChannelConfig(**configs['blue']))
colorise(m_cyan, temp, ChannelConfig(**configs['cyan']))
colorise(m_yellow, temp, ChannelConfig(**configs['yellow']))
colorise(m_magenta, temp, ChannelConfig(**configs['magenta']))

# Blend colorisation with diffuse
alpha_buf = dict()
for x in range(target_size[0]):
	for y in range(target_size[1]):
		pixel_in1 = diffuse.getpixel((x, y))
		alpha_buf[(x, y)] = pixel_in1[3]
		pixel_in1 = int3_to_float3(pixel_in1[:3])
		pixel_in1 = float3_lin_to_srgb(pixel_in1)

		pixel_in2 = temp[(x, y)]

		temp[(x, y)] = float3_mul_float3(pixel_in1, pixel_in2)

# Copy to texture
for pos, color in temp.items():
	color = float3_srgb_to_lin(color)
	color = float3_mul_float1(color, 255)
	color = (floor(color[0]), floor(color[1]), floor(color[2]), alpha_buf[pos])
	final.putpixel(pos, color)

# Save
final.save('out.png')
