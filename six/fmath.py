from typing import Tuple

def lerp(a: float, b: float, alpha: float) -> float:
	return a + b * alpha

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
