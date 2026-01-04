# Generates themes from a given palette

from random import random
from random import choice
import utils.hsl as hsl
import utils.palettes as pal
import utils.parameters as par

# select first color as "primary" color to build lightness map
def lightness_gradient(color):
    grad = []
    l_vals = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.98, 0.99, 1] # Values from Material Design's tonal map
    for l in l_vals:
        grad.append(hsl.HSL(color.h,color.s,l))
    return grad


