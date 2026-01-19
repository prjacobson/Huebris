# Huebris

An attempt at generating palettes. These will eventually be used for recoloring my background and theming apps, but for now I just want palettes.

*This work is heavily inspired by both [Coolors](https://coolors.co/) and [Material Design](https://m3.material.io/styles/color/system/how-the-system-works).*

## Scope

From a given color or (pseudo-)random color, this tool generates a palette of `N` colors and a corresponding terminal color theme. 

For each primary color in the palette, a foreground/background pairing is created with an acceptable contrast ratio.

## To-do

* [x] Convert palettes to a class
* [x] Basic terminal color generation
  * [x] Color based terminal color generation (e.g. if base is green, make red a greenish red)
  * [ ] POSTPONED Palette aware terminal color generation
    * [x] Pick colors from palette
    * [x] Skip identical (close?) hues
* [x] Foreground background generation
  * [x] ...with contrast checking
* [x] Output palette to `.json`(?) file
* [ ] More varied palette generation
  * [ ] Multistep fudging (H,S, *AND* L)
  * [ ] Non 'standard' schemes (see coolors)
* [ ] Choice of dark/light theme
* [ ] Interactive script for generation
  * [ ] Lock-able colors
  * [ ] Select new base color from given colors

## Usage

*(To be written after more is in place)*

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

