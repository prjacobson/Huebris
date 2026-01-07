# Huebris

An attempt at generating palettes. These will eventually be used for recoloring my background and theming apps, but for now I just want palettes.

*This work is heavily inspired by both [Coolors](https://coolors.co/) and [Material Design](https://m3.material.io/styles/color/system/how-the-system-works).*

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

From the "base" color that starts a palette, a terminal color scheme generated. The start color is assigned one of `[red,green,yellow,blue,magenta,cyan]` based on its hue, and the remaining colors are chosen with 60° hue rotations. Black, white, and, 'bright' color variants are generated using hardcoded lightness/saturation modifications (see `utils/parameters.py`). This system works generally, but there's some clashing when using tetradic or square color palettes.

Using [name pending], a color scheme with N base colors, lightness gradients for foreground/background selection, and a contrast checker can be generated and saved to a `.json` file.
