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
            "unidirectional" : lambda c, n, p: c.unidirectional_fudge(N=n, param=p),
            "symmetric" : lambda c, n, p: c.sym_fudge(N=n, param=p)
    }
    def expand(self,color=None,N=1,method="unidirectional",param="h"):
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
            param = choice(params) # Pick base color first
            self.expand(color=self.base_color,N=1, method="unidirectional", param=param)
            return 
        for i in range(len(color_list)):
            if i+1 == len(color_list): add_amount = to_add # last color gets all colors
            elif i == 0: add_amount = choice(list(range(1,to_add+1))) # First color always gets a use
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
    def all_colors(self):
        return [self.base_color]+self.scheme_colors+self.extra_colors
    def preview(self,verbose=False):
        print("Base color:")
        self.base_color.preview(verbose=verbose)
        print("Scheme colors:")
        for i in self.scheme_colors: i.preview(verbose=verbose)
        print("Extra colors:")
        for i in self.extra_colors: i.preview(verbose=verbose)

# All palette schemes    
palette_schemes = {
    "complementary" : lambda c,p,n: c.complementary(perfect=p),
    "split_complementary" : lambda c,p,n: c.split_complementary(perfect=p),
    "analogous" : lambda c,p,n: c.analogous(perfect=p),
    "triadic" : lambda c,p,n: c.triadic(perfect=p),
    "square" : lambda c,p,n: c.square(perfect=p),
    "tetradic" : lambda c,p,n: c.tetradic(perfect=p),
    "monochromatic" : lambda c,p,n: c.monochromatic(count=n-1,perfect=p)
}
# Generate a palette given a base color and scheme
def generate_palette(base, scheme: str,N=4,perfect=True):
    if N is None:
        N = 4
    scheme_colors = []
    try: 
        colors = palette_schemes[scheme](base,perfect,N)
        if type(colors) == hsl.HSL:
            scheme_colors.append(colors)
        else:
            scheme_colors.extend(colors)
        return palette(base,scheme_colors,scheme)
    except KeyError:
         raise ValueError(f"Unknown palette scheme: {scheme}")

# Get random palette
def random_palette(base=None,scheme=None,weighted=False,preferential=False,N=None,perfect=True):
    # Preferential list
    preferential_schemes = ["complementary"]*par.complementary_amt+["split_complementary"]*par.split_complementary_amt+["analogous"]*par.analogous_amt+["triadic"]*par.triadic_amt+["square"]*par.square_amt+["tetradic"]*par.tetradic_amt+["monochromatic"]*par.monochromatic_amt
    if base is None:
        if weighted:
            base = hsl.weighted_HSL()
        else:
            base = hsl.random_HSL()
    scheme_choices = list(palette_schemes.keys())
    if N is not None:
        try:
            int(N)
        except ValueError:
            pass
        else:
            N = int(N) # Check for float
            if N < 1:
                print(f"N < 1 unsupported, found N = {N}. Setting N to 1")
                N = 1
            match(N): # Pick palettes that work
                case _ if N == 1:
                    scheme_choices = ['monochromatic']
                case _ if N == 2:
                    scheme_choices = ['monochromatic','complementary']
                case _ if N == 3:
                    scheme_choices = ['monochromatic', 'complementary', 'triadic', 'analogous','split_complementary']
                case _ if N > 3:
                    pass
    if scheme is not None:
        if scheme in scheme_choices:
            pass
        else:
            print("Chosen scheme not compatible with palette size")
            scheme = None
    if scheme is None:
        if preferential:
            while not scheme in scheme_choices:
                scheme = choice(preferential_schemes)
        else:
            scheme = choice(scheme_choices)
    palette = generate_palette(base,scheme,N,perfect=perfect)
    return palette


# Function to get a random palette of size N
def N_palette(N=5,base=None,scheme=None,weighted=False,preferential=False,perfect=True):
    pal = random_palette(base=base,scheme=scheme,weighted=weighted,preferential=preferential,N=N,perfect=perfect)
    pal.expand_to_N(N)
    return pal
