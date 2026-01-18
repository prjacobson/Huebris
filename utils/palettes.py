# Generates palettes of colors and expands palettes to arbitrary size

from random import random
from random import choice
from random import gauss
from random import expovariate
from math import floor
import copy
import utils.hsl as hsl
import utils.parameters as par

class palette:

    def __init__(self,base_color,scheme_colors,scheme: str):
        self.base_color = base_color # Starting color
        self.scheme_colors = scheme_colors # starting colors
        self.scheme = scheme # color scheme method used
        self.extra_colors = [] # No extra colors at start 

    # Expand palette
    expansion_methods = {
            "unidirectional" : lambda c, n, p: c.N_fudge(N=n, param=p),
            "symmetric" : lambda c, n, p: c.sym_fudge(N=n, param=p)
    }
    def expand(self, color=None,N=1,method="unidirectional",param="h"):
        if color is None:
            color = choice([self.base_color]+self.scheme_colors)
        # Feels sketchy having no return but okay 
        self.extra_colors.extend(self.expansion_methods[method](color,N,param))
    # add extra colors to size N
    def expand_to_N(self, size=5):
        params = ["h", "s", "l"]
        methods = list(self.expansion_methods.keys())
        color_list = [self.base_color]+self.scheme_colors
        # Only expand off of original colors
        to_add = size-len(color_list)
        # Check
        if to_add <= 0:
            return 
        # If only need one, have to expand unidirectionally 
        if to_add == 1:
            param = choice(params)
            self.expand(color=None,N=1, method="unidirectional", param=param)
            return 
        for i in range(len(color_list)):
            if i+1 == len(color_list): add_amount = to_add # last color gets all colors
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
            self.expand(color=color_list[i],N=add_amount,method=method,param=param)
    def preview(self,verbose=False):
        print("Base color:")
        self.base_color.preview(verbose=verbose)
        print("Scheme colors:")
        for i in self.scheme_colors: i.preview(verbose=verbose)
        print("Extra colors:")
        for i in self.extra_colors: i.preview(verbose=verbose)

# All palette schemes    
palette_schemes = {
    "complementary" : lambda c: c.complementary(),
    "split_complementary" : lambda c: c.split_complementary(),
    "analogous" : lambda c: c.analogous(),
    "triadic" : lambda c: c.triadic(),
    "square" : lambda c: c.square(),
    "tetradic" : lambda c: c.tetradic(),
    "monochromatic" : lambda c: c.monochromatic()
}
# Preferential list
preferential_schemes = ["complementary"]*par.complementary_amt+["split_complementary"]*par.split_complementary_amt+["analogous"]*par.analogous_amt+["triadic"]*par.triadic_amt+["square"]*par.square_amt+["tetradic"]*par.tetradic_amt+["monochromatic"]*par.monochromatic_amt
# Generate a palette given a base color and scheme
def generate_palette(base: HSL, scheme: str):
    scheme_colors = []
    try: 
        colors = palette_schemes[scheme](base)
        if type(colors) == hsl.HSL:
            scheme_colors.append(colors)
        else:
            scheme_colors.extend(colors)
        print("base")
        print(base)
        print("scheme")
        print(scheme_colors)
        print("scheme used")
        print(scheme)
        return palette(base,scheme_colors,scheme)
    except KeyError:
         raise ValueError(f"Unknown palette scheme: {scheme}")

# Get random palette
def random_palette(base=None,scheme=None,weighted=False,preferential=False):
    if base is None:
        if weighted:
            base = hsl.weighted_HSL()
        else:
            base = hsl.random_HSL()
    if scheme is None:
        if preferential:
            scheme = choice(preferential_schemes)
        else:
            scheme = choice(list(palette_schemes.keys()))
    palette = generate_palette(base,scheme)
    return palette


# Function to get a random palette of size N
def N_palette(N=5,base=None,scheme=None,weighted=False,preferential=False):
    pal = random_palette(base=base,scheme=scheme,weighted=weighted,preferential=preferential)
    pal.expand_to_N(N)
    return pal
