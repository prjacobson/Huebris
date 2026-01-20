## Holds the theme class and exports to json

import utils.hsl as hsl
import utils.palettes as pal
import utils.term as term
import utils.parameters as par
import json

class theme:

    def __init__(self,palette,terminal):
        self.palette = palette # Palette
        terminals = [term.switch_dark_light(palette.base_color, terminal),terminal]
        dark_terminal_index = terminals[0].bg.l > terminals[1].bg.l
        self.terminal = terminals[not dark_terminal_index]
        self.dark_terminal = terminals[dark_terminal_index]
        self.base_color = self.palette.base_color

    # Preview contents
    def preview(self,term_verbose=True):
        print("Palette:")
        for i in self.palette.all_colors(): i.preview()
        print("\nTerminal:")
        self.terminal.preview(verbose=term_verbose)
        print("Dark theme terminal:")
        self.dark_terminal.preview(verbose=term_verbose)

    # Save to json file
    def save_to_json(self,filename='theme'):
        palette_dict = {
                "Base" : self.palette.base_color.hexed(),
                "Scheme colors" : [i.hexed() for i in self.palette.scheme_colors],
                "Extra colors" : [i.hexed() for i in self.palette.extra_colors],
                "Scheme" : self.palette.scheme
        }
        term_dict = {
                "Normal colors" : [i.hexed() for i in self.terminal.normal_colors],
                "Bright colors" : [i.hexed() for i in self.terminal.bright_colors],
                "fg" : self.terminal.fg.hexed(),
                "bg" : self.terminal.bg.hexed()
        }
        dark_term_dict = {
                "Normal colors" : [i.hexed() for i in self.dark_terminal.normal_colors],
                "Bright colors" : [i.hexed() for i in self.dark_terminal.bright_colors],
                "fg" : self.dark_terminal.fg.hexed(),
                "bg" : self.dark_terminal.bg.hexed()
                }
        theme_dict = {
                "Palette" : palette_dict,
                "Terminal" : term_dict,
                "Dark terminal" : dark_term_dict
        }
        with open(filename+'.json', 'w') as f:
            f.write(json.dumps(theme_dict, indent=4, ensure_ascii=False))
