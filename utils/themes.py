# Generates themes from a given palette

from random import random
from random import choice
from math import floor
import copy
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

# Get terminal colors 
def get_term_colors(color,preview=False):
    # Weird structure so I can flip bright/normal if need be
    color.l = min(color.l,par.term_max_brightness)
    red, green, yellow, blue, magenta, cyan = [],[],[],[],[],[]
    red.append(color.get_named_color('red'))
    green.append(color.get_named_color('green'))
    yellow.append(color.get_named_color('yellow'))
    blue.append(color.get_named_color('blue'))
    magenta.append(color.get_named_color('magenta'))
    cyan.append(color.get_named_color('cyan'))
    # If base color too light, darken instead
    directions = [-1,1]
    lighten_dir = directions[color.l+par.bright_lighten<1]
    red.append(red[0].lighten(lighten_dir*par.bright_lighten))
    green.append(green[0].lighten(lighten_dir*par.bright_lighten)) 
    yellow.append(yellow[0].lighten(lighten_dir*par.bright_lighten))
    blue.append(blue[0].lighten(lighten_dir*par.bright_lighten))
    magenta.append(magenta[0].lighten(lighten_dir*par.bright_lighten))
    cyan.append(cyan[0].lighten(lighten_dir*par.bright_lighten))
    # If darkened, flip normal and bright
    if lighten_dir == -1:
        for c in [red, green, yellow, blue, magenta, cyan]:
            c[0].s = c[0].s*par.bright_saturate_percentage
            c.reverse()
    # black and white
    base_hue = color.h
    black = [hsl.HSL(base_hue,par.black_saturation,par.black_lightness),hsl.HSL(base_hue,par.bright_black_saturation,par.bright_black_lightness)]
    white = [hsl.HSL(base_hue,par.white_saturation,par.white_lightness),hsl.HSL(base_hue,par.bright_white_saturation,par.bright_white_lightness)]
    term_colors = [black,red,green,yellow,blue,magenta,cyan,white]
    term_colors = [shade for color in term_colors for shade in color]
    if preview:
        def term_color_preview(color):
            r,g,b = color.to_RGB()
            hexed = lambda c : hex(floor(c/1))[2:].zfill(2)
            return (f"\033[48;2;{r};{g};{b}m #{hexed(r)}{hexed(g)}{hexed(b)} \033[0m")
        # even indices = normal colors, do first
        normals = ""
        evens = range(len(term_colors))[::2]
        for i in evens:
            normals = normals+term_color_preview(term_colors[i])
        normals = normals + "\n"
        brights = ""
        odds = range(len(term_colors))[1::2]
        for i in odds:
            brights = brights+term_color_preview(term_colors[i])
        brights = brights + "\n"
        preview_text = normals+brights
        print(preview_text)
    return term_colors
