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
            return (f"\033[48;2;{r};{g};{b}m #{color.hexed()} \033[0m")
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
# Given a set of 6 colors, create paired bright/dark colors
def get_matched_term_colors(term_colors):
    term_colors
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
# Basic doesn't account for color scheme, just goes off a base color (usually first primary color) with 60degree rotations
def get_basic_term_colors(base):
    # Weird structure so I can flip bright/normal if need be
    color = hsl.HSL(base.h,base.s,min(base.l,par.term_max_brightness))
    color_set_1 = []
    for c in hsl.named_colors:
        color_set_1.append(color.get_named_color(c))
    # get normal/bright colors
    normal, bright = get_matched_term_colors(color_set_1)
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
def get_colored_term_colors(base):
   return None 
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
