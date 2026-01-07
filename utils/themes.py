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

# Get terminal colors 
def get_term_colors(color):
    # Weird structure so I can flip bright/normal if need be
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
    term_colors = [red,green,yellow,blue,magenta,cyan]
    term_colors = [shade for color in term_colors for shade in color]
    return term_colors
