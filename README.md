# Huebris

An attempt at generating palettes. These will eventually be used for recoloring my background and theming apps, but for now I just want palettes.

*This work is heavily inspired by both [Coolors](https://coolors.co/) and [Material Design](https://m3.material.io/styles/color/system/how-the-system-works).*

## HSL but make it swag

Material design introduces **HCT** (Hue Chroma Tone), a variation on HSL (Hue Saturation Lightness). 
While saturation ~ how colorful something is, it fails to account for the lightness. That is, fully saturated colors can appear white or black if they have sufficiently extreme lightness. 
I don't want to get that complex, but I do want to do better than HSL. I've added a "vividness" value, calculated from the saturation and lightness.

*Note, I haven't come up with an expression for $V$ yet. Some notes:*
* When $S$ is low, $L$ doesn't affect the color much, so $V$ should be close to $S$ at low $S$
* $V$ should be symmetric about $L=0.5$. this may not follow real color principles, but that's fine
* I don't care what $V$'s limits are, but the conversion back to $S$ should never put $S$ outside $\langle 0,1 \rangle$
