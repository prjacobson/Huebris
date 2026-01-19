# Generates terminal colors

from random import random
from random import choice
from math import floor
import copy
import utils.hsl as hsl
import utils.palettes as pal
import utils.parameters as par

### Define terminal class
class terminal_colors:

    def __init__(self,normal_colors,bright_colors,bg,fg):
        self.normal_colors = normal_colors
        self.bright_colors = bright_colors
        self.fg = fg
        self.bg = bg

    def preview(self):
        def term_color_preview(color):
            r,g,b = color.to_RGB()
            return (f"\033[48;2;{r};{g};{b}m #{color.hexed()} \033[0m")
        bg_fg = term_color_preview(self.bg)+term_color_preview(self.fg)+"\n"
        normals = ""
        for i in range(len(self.normal_colors)):
            normals = normals+term_color_preview(self.normal_colors[i])
        normals = normals + "\n"
        brights = ""
        for i in range(len(self.bright_colors)):
            brights = brights+term_color_preview(self.bright_colors[i])
        brights = brights + "\n"
        preview_text = "bg&fg:\n"+bg_fg+"Term. colors:\n"+normals+brights
        print(preview_text)

### Foreground background function
def full_lightness_gradient(color):
    grad = []
    l_vals = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.98, 0.99, 1] # Values from Material Design's tonal map
    for l in l_vals:
        grad.append(hsl.HSL(color.h,color.s,l))
    return grad
def darkness_gradient(color):
    grad = []
    l_vals = [0.50 - (i*0.025) for i in range(21)]
    for l in l_vals:
        grad.append(hsl.HSL(color.h,color.s,l))
    return grad
def lightness_gradient(color):
    grad = []
    l_vals = [0.50 + (i*0.025) for i in range(21)]
    for l in l_vals:
        grad.append(hsl.HSL(color.h,color.s,l))
    return grad
# Background and foreground w/ contrast check
def bg_fg(base,term_colors,bg_fg_contrast=par.bg_fg_contrast, bg_color_contrast=par.bg_color_contrast):
    # Remove b&w from term_colors
    colors = []
    for i in range(1,len(term_colors)):
        colors.append(term_colors[i])
    # Check whether to switch to light mode
    if min([i.l for i in colors]) < par.dark_mode_cutoff:
        bg_grad = lightness_gradient(base)
        fg = hsl.HSL(base.h,base.s,0.1)
    else:
        bg_grad = darkness_gradient(base)
        fg = hsl.HSL(base.h,base.s,0.98)
    bg_i = 0
    for i in range(len(bg_grad)):
        bg_i = i
        fg_cr = hsl.contrast_ratio(bg_grad[i],fg)
        color_cr = [hsl.contrast_ratio(bg_grad[i],c) for c in colors]
        if fg_cr > bg_fg_contrast and min(color_cr) > bg_color_contrast:
            break
    bg = bg_grad[bg_i]
    return bg, fg

### Terminal colors 
## Utilities
# Given a set of 6 colors, create paired bright/dark colors
def matched_term_colors(term_colors):
    # check each color individually
    normal = []
    bright = []
    for c in term_colors:
        color = hsl.HSL(c.h,c.s,min(c.l,par.term_max_brightness))
        darken = color.l+par.bright_lighten>par.term_max_brightness
        lighten_dir = [1,-1][darken]
        if darken:
            bright.append(color)
            normal.append(color.lighten(lighten_dir*par.bright_lighten))
        else:
            normal.append(color)
            bright.append(color.lighten(lighten_dir*par.bright_lighten))
    for c in bright:
        c.s = c.s*par.bright_saturate_percentage
    return normal, bright
# Get white and black from a base color
def white_black_term_colors(base):
    # black and white
    base_hue = base.h
    black = hsl.HSL(base_hue,par.black_saturation,par.black_lightness)
    bright_black = hsl.HSL(base_hue,par.bright_black_saturation,par.bright_black_lightness)
    white = hsl.HSL(base_hue,par.white_saturation,par.white_lightness)
    bright_white = hsl.HSL(base_hue,par.bright_white_saturation,par.bright_white_lightness)
    return black, bright_black, white, bright_white
## Functions for full terminal colors
# Basic doesn't account for color scheme, just goes off a base color (usually first primary color) with 60degree rotations
def basic_term_colors(base):
    # Weird structure so I can flip bright/normal if need be
    color = hsl.HSL(base.h,base.s,max(par.term_min_brightness,min(base.l,par.term_max_brightness)))
    color_set_1 = []
    for c in hsl.named_colors:
        color_set_1.append(color.rotate_to_named_color(c))
    # get normal/bright colors
    normal, bright = matched_term_colors(color_set_1)
    black, bright_black, white, bright_white = white_black_term_colors(base)
    normal.insert(0,black)
    normal.append(white)
    bright.insert(0,bright_black)
    bright.append(bright_white)
    bg, fg = bg_fg(base,normal)
    return terminal_colors(normal,bright,bg,fg)
# Colored will take a base color  and decolor/recolor, so your red may be reddish green if you start with green
def colored_term_colors(base,amt=par.colorize_amt):
    base_color = hsl.HSL(base.h,base.s,max(par.term_min_brightness,min(base.l,par.term_max_brightness)))
    colors = list(hsl.named_colors.keys())
    base_color_name = base_color.closest_named_color()
    term_dict = {}
    # Pick colorization amount based on lightness
    lightness_amt = floor(abs(base_color.l-0.5)/0.125)+1
    # Decolor the base
    decolor = base_color.colorize(base_color_name,amt=-amt/lightness_amt)
    for c in colors:
        term_dict[c] = decolor.colorize(c,amt=amt/lightness_amt)
    # reset base color
    term_dict[base_color_name] = base_color
    term_color_list = [term_dict[i] for i in colors]
    normal, bright = matched_term_colors(term_color_list)
    black, bright_black, white, bright_white = white_black_term_colors(base)
    normal.insert(0,black)
    normal.append(white)
    bright.insert(0,bright_black)
    bright.append(bright_white)
    bg, fg = bg_fg(base,normal)
    return terminal_colors(normal,bright,bg,fg)

# Dark mode <-> Light mode
def switch_dark_light(base,term:terminal_colors):
    flip = lambda c: hsl.HSL(c.h,c.s,-(c.l-0.5)+0.5)
    flipped_normal = [flip(c) for c in term.normal_colors]
    flipped_bright = [flip(c) for c in term.bright_colors] # Flipped bright will be darker than flipped normal
    normal, bright = flipped_bright, flipped_normal # matched_term_colors(flipped_colors)
    black, bright_black, white, bright_white = white_black_term_colors(base)
    normal[0]=black
    normal[len(term.normal_colors)-1]=white
    bright[0]=bright_black
    bright[len(term.normal_colors)-1]=bright_white
    bg, fg = bg_fg(base,normal)
    return terminal_colors(normal,bright,bg,fg)
'''
# Not functioning, can't figure out a good way to fill in colors without overcomplicating
# Palette will select the first colors from the primary colors and use similar differences
def get_palette_term_colors(pal):
    # Get distances from pure color
    distance_dict = {}
    color_options = pal.primary_colors+pal.extra_colors
    # Elimate identical hues
    hues = [i.h for i in color_options]
    dupes = []
    # Slow but fine at this size
    for h in range(len(hues)):
        for i in range(h+1,len(hues)):
            if min(abs(hues[h]-hues[i]),360-abs(hues[h]-hues[i])) < par.palette_term_hue_range:
                dupes.append(i)
    dupes = list(set(dupes)) # Remove dupes
    dupes.sort(reverse=True) # Remove from end backwards
    for i in dupes: color_options.pop(i)
    for name in hsl.named_colors:
        name_distances = []
        for c in color_options:
            name_distances.append(c.get_named_color_distance(name))
        distance_dict[name] = name_distances
    # Also get dicts of distances to each named color for every color option
    color_option_distances = []
    for p in range(len(color_options)):
        name_distances = {}
        for name in hsl.named_colors:
            name_distances[name] = distance_dict[name][p]
        color_option_distances.append(name_distances)
    # Select best fit for colors (or no fit)
    # Select a color for name if a) color is closest to name b) name is the closest named color
    # Maybe jank? But works.
    term_picks = {}
    fitting_colors = True # you always start with at least one fitting color
    while fitting_colors:
        colors_found = []
        indexes_to_delete = []
        for c in distance_dict:
            closest_dist = min(distance_dict[c])
            best_fit_index = distance_dict[c].index(closest_dist)
            if closest_dist < par.palette_term_hue_range:
                if closest_dist == min(color_option_distances[best_fit_index].values()):
                    print("assigning " + c)
                    term_picks[c] = color_options[best_fit_index]
                    # Stop searching for this color
                    colors_found.append(c)
                    # Remove this palette color from the colors we're selecting from
                    # Remove this palette's distances from the distance dict
                    indexes_to_delete.append(best_fit_index)
        # Stop searching for this color
        for found in colors_found:
            distance_dict.pop(found) # Stop searching for this terminal color
            for c in color_option_distances:
                c.pop(found)
        # Remove these colors from color options
        for index in sorted(indexes_to_delete, reverse = True): # Reverse so we delete from end
            del color_options[index]
            del color_option_distances[index]
            # Remove these distances from distance dict
            for c in distance_dict:
                del distance_dict[c][index]
        # Update whether any colors fit
        if len(color_options) != 0:
            all_distances = [dist for dists in distance_dict.values() for dist in dists]
            fitting_colors = min(all_distances) < par.palette_term_hue_range
        else: fitting_colors = False
    # Fill in other colors
    # TODO
    return distance_dict,color_option_distances,term_picks
'''
