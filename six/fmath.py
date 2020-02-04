from typing import Tuple
from math import floor

Int3 = Tuple[int, int, int]
Float3 = Tuple[float, float, float]

LUMINANCE = [0.3, 0.59, 0.11]

class _Float3Proxy(object):
	__slots__ = ('r', 'g', 'b')

	def __init__(self, value: Float3):
		self.r = value[0]
		self.g = value[1]
		self.b = value[2]

def int3_to_float3(pixel: Int3) -> Float3:
	return (
		pixel[0] / 255,
		pixel[1] / 255,
		pixel[2] / 255,
	)

def float1_lin_to_srgb(linear: float) -> float:
	if linear < 0.00313067:
		return linear * 12.92
	return (linear ** (1.0 / 2.4)) * 1.055 - 0.055

def float3_lin_to_srgb(linear: Float3) -> Float3:
	linear = _Float3Proxy(linear)
	return (
		float1_lin_to_srgb(linear.r),
		float1_lin_to_srgb(linear.g),
		float1_lin_to_srgb(linear.b),
	)

def float1_srgb_to_lin(color: float) -> float:
	color = max(6.10352e-5, color)
	return ((color * (1.0 / 1.055) + 0.0521327) ** 2.4) if color > 0.04045 else color * (1.0 / 12.92)

def float3_srgb_to_lin(color: Float3) -> Float3:
	color = _Float3Proxy(color)
	return (
		float1_srgb_to_lin(color.r),
		float1_srgb_to_lin(color.g),
		float1_srgb_to_lin(color.b),
	)

def float1_lerp(a: float, b: float, alpha: float) -> float:
	return a * (1 - alpha) + b * alpha

def float3_lerp(a: Float3, b: Float3, alpha: float) -> Float3:
	a = _Float3Proxy(a)
	b = _Float3Proxy(b)
	return (
		float1_lerp(a.r, b.r, alpha),
		float1_lerp(a.g, b.g, alpha),
		float1_lerp(a.b, b.b, alpha),
	)

def float1_clamp(min_val: float, value: float, max_val: float) -> float:
	return min(max_val, max(value, min_val))

def float3_clamp(min_val: float, value: Float3, max_val: float) -> Float3:
	value = _Float3Proxy(value)
	return (
		float1_clamp(min_val, value.r, max_val),
		float1_clamp(min_val, value.g, max_val),
		float1_clamp(min_val, value.b, max_val),
	)

def float3_get_luminance(color: Float3) -> float:
	color = _Float3Proxy(color)
	Lr = color.r * LUMINANCE[0]
	Lg = color.g * LUMINANCE[1]
	Lb = color.b * LUMINANCE[2]
	return Lr + Lg + Lb

def float3_min(a: Float3, b: Float3) -> Float3:
	a = _Float3Proxy(a)
	b = _Float3Proxy(b)
	return (
		a.r if a.r < b.r else b.r,
		a.g if a.g < b.g else b.g,
		a.b if a.b < b.b else b.b,
	)

def float3_mul_float1(a: Float3, b: float) -> Float3:
	a = _Float3Proxy(a)
	return (
		a.r * b,
		a.g * b,
		a.b * b,
	)

def float3_mul_float3(a: Float3, b: Float3) -> Float3:
	a = _Float3Proxy(a)
	b = _Float3Proxy(b)
	return (
		a.r * b.r,
		a.g * b.g,
		a.b * b.b,
	)

def float3_add_float3(a: Float3, b: Float3) -> Float3:
	a = _Float3Proxy(a)
	b = _Float3Proxy(b)
	return (
		a.r + b.r,
		a.g + b.g,
		a.b + b.b,
	)

#def desaturate(color: Float3, percent: float) -> float:
#	L = float3_get_luminance(color)
#	r = color[0] + percent * (L - color[0])
#	g = color[1] + percent * (L - color[1])
#	b = color[2] + percent * (L - color[2])
#	return (r, g, b)

#def choose_darker(pixel_a: Tuple[int, int, int], pixel_b: Tuple[int, int, int]) -> Tuple[int, int, int]:
#	La = get_brightness(pixel_a)
#	Lb = get_brightness(pixel_b)
#	if La < Lb:
#		return pixel_a
#	return pixel_b
