# Huebris

An attempt at generating palettes. These will eventually be used for recoloring my background and theming apps, but for now I just want palettes.

*This work is heavily inspired by both [Coolors](https://coolors.co/) and [Material Design](https://m3.material.io/styles/color/system/how-the-system-works).*

## Scope

From a given color or (pseudo-)random color, this tool generates a palette of `N` colors and a corresponding dark and light terminal color theme. 

For the base color of the palette, a foreground/background pairing is created with an acceptable contrast ratio (see [Quirks](##Quirks)).

## To-do

* [x] Convert palettes to a class
* [x] Basic terminal color generation
  * [x] Color based terminal color generation (e.g. if base is green, make red a greenish red)
  * [ ] POSTPONED Palette aware terminal color generation
    * Most palettes perfectly spread by `n*60°` anyways, further implementation would be complex and annoying
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
* [ ] Interactive script for generation
  * [ ] Select new base color from given colors
  * [ ] Lock-able colors

## Usage

*(To be written after more is in place)*


## Quirks

Here's some things you may notice in generating your palettes:
* Color quirks
  * N/A currently
* Palette quirks
  * N/A currently
* Terminal quirks
  * Sometimes dark mode/light mode are near identical
    * This is because dark/light flips the colors over `lightness = 0.5`, so values close to that won't change much
  * The background/color contrast requirement of 2.0 is lower than (Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG21/) recommendation of 3.0 for large text and 4.5 for normal text.
    * Even still, the background of 'dark mode' is often set to `#000000` because a high contrast can't be achieved with the given colors

## How

From a base color (which can be randomly or pseudorandomly generated), a basic palette is generated using one of the following methods:
* Complementary colors
* Split-complementary colors
* Analogous colors
* Triadic colors
* Square colors
* Tetradic colors
* Monochromatic colors

There are 3 levels of randomness in palette generation.

| Generator | Color selection | Scheme selection |
| --- | --- | --- |
| `random` | Random `H`, `S`, and `L` | Random choice |
| `weighted` | Random `H`, `S` weighted towards 1, `L` weighted towards 0.5 | Random choice |
| `preferential` | *Same as* `weighted` | Biased towards more conventional schemes |

[NOT YET IMPLEMENTED] Also, some imperfection (changing of `H`, `S`, and/or `L`) is added to zhuzh it up. This can be disabled by using the `perfect=True` flag in palette generation.
