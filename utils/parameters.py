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
l_bound = 0.1 

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

# Theme options
bright_lighten = 0.2 # how much to lighten for 'bright' colors
bright_saturate_percentage = .9 # how much to desaturate bright color
