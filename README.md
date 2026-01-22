# Huebris

An attempt at generating palettes. These will eventually be used for recoloring my background and theming apps, but for now I just want palettes.

*This work is heavily inspired by both [Coolors](https://coolors.co/) and [Material Design](https://m3.material.io/styles/color/system/how-the-system-works).*

## Scope

From a given color or (pseudo-)random color, this tool generates a palette of `N` colors and a corresponding dark and light terminal color theme. 

For the base color of the palette, a foreground/background pairing is created with an acceptable contrast ratio (see [Quirks](#quirks)).

## Usage

The interactive generation script can be run with
```
python huebris.py
```
For simple generation of a random palette or theme, use

```
python -m generators.palette 
    -b [base color] 
    -s [scheme] 
    -w [weighted] 
    -p [preferential] 
    -n [num. of colors]
```
or
```
python -m generators.theme 
    [all options from generators.palette]
    -t [terminal scheme]
```

### Requirements

* This script makes use of `random`, `math`, `json`, and `dataclasses`
* Use of the python `match case` syntax requires `python>=3.10.*`
* It will help to use a terminal with support for 256 colors

## How

From a base color (which can be randomly or pseudorandomly generated), a basic palette is generated using one of the following methods:
* Complementary colors
* Split-complementary colors
* Analogous colors
* Triadic colors
* Square colors
* Tetradic colors
* Monochromatic colors

There are 2 degrees of randomness in palette generation
* `weighted`: less random base color
  * Random `H`, `S` weighted towards 1, `L` weighted towards 0.5
* `preferential`: less random color scheme
  * Biased towards more 'conventional' schemes

[NOT YET IMPLEMENTED] Also, some imperfection (changing of `H`, `S`, and/or `L`) is added to zhuzh it up. This can be disabled by using the `perfect=True` flag in palette generation.

There are 2 methods of generating terminal color palettes. Both methods start with determining which color (of red, green, yellow, blue, magenta, cyan) the base color is closest to.
* `basic`: even spacing
  * Rotates the hue of the base color by `N*60°` to get the remaining colors
* `colored`: similar hues
  * 'decolors' the base color (e.g., makes it less green), then shifts this decolored hue towards the remaining 5 terminal colors

## Quirks

Here's some things you may notice in generating your palettes:
* Color quirks
  * N/A currently
* Palette quirks
  * N/A currently
* Terminal quirks
  * Only uses a base color, no consideration for rest of palette
  * Sometimes dark mode/light mode are near identical
    * This is because dark/light flips the colors over `lightness = 0.5`, so values close to that won't change much
  * The background/color contrast requirement of 2.0 is lower than [Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG21/) recommendation of 3.0 for large text and 4.5 for normal text.
    * Even still, the background of 'dark mode' is often set to `#000000` because a high contrast can't be achieved with the given colors

## To-do

* [x] Convert palettes to a class
* [x] Basic terminal color generation
  * [x] Color based terminal color generation (e.g. if base is green, make red a greenish red)
  * [ ] POSTPONED Palette aware terminal color generation
    * Most palettes perfectly spread by `n*60°`, so `basic_term_colors` is easy
    * Not sure how best to work with `colored_term_colors`. Need to think on
    * [x] Pick colors from palette
    * [x] Skip identical (close?) hues
* [x] Foreground background generation
  * [x] ...with contrast checking
* [x] Output palette to `.json`(?) file
* [ ] More varied palette generation
  * [ ] Multistep fudging (H,S, *AND* L)
  * [ ] Non 'standard' schemes (see coolors)
* [ ] Choice of dark/light theme
  * [x] Dark/light terminal options
    * [ ] Brighten/darken term colors to fit?
* [x] Use compatible scheme for N colors
* [x] Interactive script for generation
  * [x] Select new base color from given colors
  * [ ] Lock-able colors
  * [ ] Quicker random generation of full themes
* [x] Command to get random palette (using argparse for arguments)

### Bugs
* Dark mode/Light mode generation is shoddy
  * Occasionally both backgrounds are `#000000`
  * Contrast requirements are forcing a lot of `#000000` or `#ffffff` backgrounds
