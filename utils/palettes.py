from random import random
from random import choice
from random import gauss
from random import expovariate
from math import floor
from utils.hsl import HSL

#Palettes
palette_schemes = {
    "complementary" : lambda c: c.complementary(),
    "split_complementary" : lambda c: c.split_complementary(),
    "analogous" : lambda c: c.analogous(),
    "triadic" : lambda c: c.triadic(),
    "square" : lambda c: c.square(),
    "tetradic" : lambda c: c.tetradic(),
    "monochromatic" : lambda c: c.monochromatic()
}
def generate_palette(base: HSL, scheme: str):
    palette = [base]
    try: 
        colors = palette_schemes[scheme](base)
        if type(colors) == HSL:
            palette.append(colors)
        else:
            palette.extend(colors)
        return palette
    except KeyError:
         raise ValueError(f"Unknown palette scheme: {scheme}")

# Get random palette
def random_palette(preview=False):
    base = HSL(random()*360,random(),random())
    method = choice(list(palette_schemes.keys()))
    palette = generate_palette(base,method)
    if preview:
        for i in palette: i.preview()
    return palette
# palette with base color weighted for high saturation medium lightness
def weighted_palette(preview=False):
    saturation_mean = 0.75
    lightness_mean = 0.5
    lightness_var = 0.25
    saturation = -1
    lightness = -1
    while saturation<0 or 1<saturation:
        saturation = 1-expovariate(1/(1-saturation_mean))
    while lightness<0 or 1<lightness:
        lightness = gauss(lightness_mean,lightness_var)
    base = HSL(random()*360,saturation,lightness)
    method = choice(list(palette_schemes.keys()))
    palette = generate_palette(base,method)
    if preview:
        for i in palette: i.preview()
    return palette
