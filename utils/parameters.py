# Stores parameter values used across files for easier modification

# Colorscheme options
monochrome_range = 0.25

# Fudge Options
hue_fudge = 30 # Max fudge of hue
min_hue_fudge = 5
sat_fudge = 0.4 # Max fudge of saturation
min_sat_fudge = 0.15
light_fudge = 0.3 # Max fudge of lightness
min_light_fudge = 0.05
# Careful to never make min_fudge > bound
s_bound = 0.15 # how close to bounds to force a direction
l_bound = 0.15 
# How much to prefer saturation or lightness for imperfect palettes
imperfect_saturation = 3
imperfect_lightness = 2
imperfect_hue_fudge = 5
imperfect_sat_fudge = 0.1
imperfect_light_fudge = 0.1

# Weighted palette options
saturation_mean = 0.75
lightness_mean = 0.5
lightness_var = 0.25
# Preferential palette weights
complementary_amt = 3
split_complementary_amt = 3
analogous_amt = 3
triadic_amt = 2
square_amt = 1
tetradic_amt = 2
monochromatic_amt = 1

# Term options
term_min_brightness = 0.1
term_max_brightness = 0.9
bright_lighten = 0.2 # how much to lighten for 'bright' colors
bright_saturate_percentage = .9 # how much to desaturate bright color
black_saturation = 0.12
bright_black_saturation = 0.15
black_lightness = 0.05
bright_black_lightness = 0.20
white_saturation = 0.05
bright_white_saturation = 0.02
white_lightness = 0.7
bright_white_lightness = 0.9
colorize_amt = 100
dark_mode_cutoff = 0.15
bg_fg_contrast = 4.5
bg_color_contrast = 2.5
palette_term_hue_closeness = 10 # how close can palette hues be
palette_term_hue_range = 60 # how far away a hue can be from a 'standard' terminal color
