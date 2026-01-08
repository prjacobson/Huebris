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

class terminal_colors:

    def __init__(self,normal_colors,bright_colors):
        self.normal_colors = normal_colors
        self.bright_colors = bright_colors

    def preview(self):
        def term_color_preview(color):
            r,g,b = color.to_RGB()
            hexed = lambda c : hex(floor(c/1))[2:].zfill(2)
            return (f"\033[48;2;{r};{g};{b}m #{hexed(r)}{hexed(g)}{hexed(b)} \033[0m")
        normals = ""
        for i in range(len(self.normal_colors)):
            normals = normals+term_color_preview(self.normal_colors[i])
        normals = normals + "\n"
        brights = ""
        for i in range(len(self.bright_colors)):
            brights = brights+term_color_preview(self.bright_colors[i])
        brights = brights + "\n"
        preview_text = normals+brights
        print(preview_text)

# Get terminal colors 
# Basic doesn't account for color scheme, just goes off first color with 60degree rotations
def get_basic_term_colors(base,preview=False):
    # Weird structure so I can flip bright/normal if need be
    color = hsl.HSL(base.h,base.s,min(base.l,par.term_max_brightness))
    color_set_1 = []
    color_set_1.append(color.get_named_color('red'))
    color_set_1.append(color.get_named_color('green'))
    color_set_1.append(color.get_named_color('yellow'))
    color_set_1.append(color.get_named_color('blue'))
    color_set_1.append(color.get_named_color('magenta'))
    color_set_1.append(color.get_named_color('cyan'))
    # If base color too light, darken instead
    darken = color.l+par.bright_lighten>par.term_max_brightness
    lighten_dir = [1,-1][darken]
    color_set_2 = []
    color_set_2.append(color_set_1[0].lighten(lighten_dir*par.bright_lighten))
    color_set_2.append(color_set_1[1].lighten(lighten_dir*par.bright_lighten))
    color_set_2.append(color_set_1[2].lighten(lighten_dir*par.bright_lighten))
    color_set_2.append(color_set_1[3].lighten(lighten_dir*par.bright_lighten))
    color_set_2.append(color_set_1[4].lighten(lighten_dir*par.bright_lighten))
    color_set_2.append(color_set_1[5].lighten(lighten_dir*par.bright_lighten))
    # If we darkened, color set 2 should be normal colors. Else color set 1
    normal = [color_set_1,color_set_2][darken]
    bright = [color_set_2,color_set_1][darken]
    for c in bright:
        c.s = c.s*par.bright_saturate_percentage
    # black and white
    base_hue = color.h
    black = hsl.HSL(base_hue,par.black_saturation,par.black_lightness)
    bright_black = hsl.HSL(base_hue,par.bright_black_saturation,par.bright_black_lightness)
    white = hsl.HSL(base_hue,par.white_saturation,par.white_lightness)
    bright_white = hsl.HSL(base_hue,par.bright_white_saturation,par.bright_white_lightness)
    normal.insert(0,black)
    normal.append(white)
    bright.insert(0,bright_black)
    bright.append(bright_white)
    return terminal_colors(normal,bright)
