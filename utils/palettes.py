# Generates palettes of colors and expands palettes to arbitrary size

from random import random
from random import choice
from random import gauss
from random import expovariate
from math import floor
import copy
from utils.hsl import HSL
import utils.parameters as par

# Unsure if palettes should be class? Maybe not
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

# Colorscheme palettes
# Get random palette
def random_palette(preview=False,base=None,method=None):
    if base is None:
        base = HSL(random()*360,random(),random())
    if method is None:
        method = choice(list(palette_schemes.keys()))
    palette = generate_palette(base,method)
    if preview:
        for i in palette: i.preview()
    return palette
# palette with base color weighted for high saturation medium lightness
def weighted_palette(preview=False,base=None,method=None):
    saturation_mean = par.saturation_mean
    lightness_mean = par.lightness_mean
    lightness_var = par.lightness_var
    saturation = -1
    lightness = -1
    while saturation<0 or 1<saturation:
        saturation = 1-expovariate(1/(1-saturation_mean))
    while lightness<0 or 1<lightness:
        lightness = gauss(lightness_mean,lightness_var)
    if base is None:
        base = HSL(random()*360,saturation,lightness)
    if method is None:
        method = choice(list(palette_schemes.keys()))
    palette = generate_palette(base,method)
    if preview:
        for i in palette: i.preview()
    return palette

# Expanding colorscheme palettes with fudging
# Expand to N total colors
expansion_methods = {
        "unidirectional" : lambda c, n, p: c.N_fudge(N=n, param=p),
        "symmetric" : lambda c, n, p: c.sym_fudge(N=n, param=p)
}
# Function to add colors to a palette
def expand_palette(pallete, color=None,N=1, method="unidirectional", param="h"):
    if color is None:
        color = choice(pallete)
    return expansion_methods[method](color,N,param)
# Function to get a palette to a certain size
def bigger_palette(palette, size=5):
    params = ["h", "s", "l"]
    methods = list(expansion_methods.keys())
    # Only expand off of original colors
    orig_palette = palette.copy()
    new_palette = []
    new_palette.extend(orig_palette)
    to_add = size-len(orig_palette)
    # Check
    if to_add <= 0:
        return new_palette
    # If only need one, have to expand unidirectionally 
    if to_add == 1:
        param = choice(params)
        new_palette.extend(expand_palette(new_palette, N=1, method="unidirectional", param=param))
        return new_palette
    for i in range(len(orig_palette)):
        if i+1 == len(orig_palette): add_amount = to_add
        else: add_amount = choice(list(range(to_add+1)))
        to_add = to_add-add_amount
        param = choice(params)
        # Check if symmetric makes sense, choose method
        if add_amount == 0: 
            continue
        if add_amount%2 == 0:
            method=choice(methods)
        else: method="unidirectional"
        if method == "symmetric": add_amount = int(add_amount/2)
        # add to palette
        new_palette.extend(expand_palette(new_palette, color=orig_palette[i],N=add_amount, method=method, param=param))
    return new_palette

# Function to get a random palette of size N
def random_N_palette(N=5,preview=False,base=None,method=None):
    base_palette = random_palette(base=base,method=method)
    N_palette = bigger_palette(base_palette,size=N)
    if preview:
        for i in N_palette: i.preview()
    return N_palette
def weighted_N_palette(N=5,preview=False,base=None,method=None):
    base_palette = weighted_palette(base=base,method=method)
    N_palette = bigger_palette(base_palette,size=N)
    if preview:
        for i in N_palette: i.preview()
    return N_palette
