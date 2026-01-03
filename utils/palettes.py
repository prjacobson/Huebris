from random import random
from random import choice
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
def get_palette(base: HSL, scheme: str):
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
    palette = get_palette(base,method)
    if preview:
        for i in palette: i.preview()
    return palette

