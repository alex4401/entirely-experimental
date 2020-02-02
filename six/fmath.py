from typing import Tuple
from math import floor

def lerp(a: float, b: float, alpha: float) -> float:
	return a * (1 - alpha) + b * alpha

def clamp(min_val: float, value: float, max_val: float) -> float:
	return min(max_val, max(value, min_val))

def get_brightness(color: Tuple[int, int, int]) -> float:
	return (color[0] * 0.3 + 0.6 * color[1] + 0.1 * color[2]) / (255 * (0.3 + 0.6 + 0.1))

def desaturate(color: Tuple[int, int, int], percent: float) -> float:
	L = get_brightness(color)
	r = color[0] + percent * (L - color[0])
	g = color[1] + percent * (L - color[1])
	b = color[2] + percent * (L - color[2])
	return (r, g, b)

def choose_darker(pixel_a: Tuple[int, int, int], pixel_b: Tuple[int, int, int]) -> Tuple[int, int, int]:
	La = get_brightness(pixel_a)
	Lb = get_brightness(pixel_b)
	if La < Lb:
		return pixel_a
	return pixel_b

def clamp_pixel(lower: int, pixel: Tuple[int, int, int], upper: int) -> Tuple[int, int, int]:
	return (clamp(lower, pixel[0], upper), clamp(lower, pixel[1], upper), clamp(lower, pixel[2], upper))

def to_pixelf(pixel: Tuple[int, int, int]) -> Tuple[float, float, float]:
	return (pixel[0] / 255, pixel[1] / 255, pixel[2] / 255)

def to_pixeli(pixel: Tuple[float, float, float]) -> Tuple[int, int, int]:
	return clamp_pixel(0, (floor(pixel[0] * 255), floor(pixel[1] * 255), floor(pixel[2] * 255)), 255)

def sum_pixels(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
	return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def mul_pixelf(a: Tuple[float, float, float], b: float):
	return (a[0] * b, a[1] * b, a[2] * b)
