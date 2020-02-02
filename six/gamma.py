from typing import Tuple

GAMMA = 2.2

def from_linear_color(value: float) -> float:
	return value ** GAMMA

def from_linear_pixelf(pixel: Tuple[float, float, float]) -> Tuple[float, float, float]:
	return (from_linear_color(pixel[0]), from_linear_color(pixel[1]), from_linear_color(pixel[2]))
