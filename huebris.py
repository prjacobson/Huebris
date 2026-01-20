import utils.hsl as hsl
import utils.palettes as pal
import utils.term as term
import utils.theme as thm
import utils.parameters as par

nr = lambda: print ("Input not recognized, try again")

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

print("Welcome to huebris!")
print("Respond 'i' to enter interactive palette builder or press [ENTER] to use defaults")
while True:
    interactive = input()
    if interactive.lower() == 'i':
        break
    if interactive == '':
        # Default settings
        base=None
        weighted = True
        preferential = True
        scheme = None
        N = 5
        print("Using default settings")
        break 
    else:
        nr()

# Interactive palette option selection
if interactive == 'i' or interactive == 'I':        
    generation_options = ["Random", "Weighted","Choose a specific color"]
    perfect_options = ["Perfect", "Imperfect"]
    palette_options = ["Random", "Pseudorandom (biased)", "Choose a specific scheme"]
    scheme_options = list(pal.palette_schemes.keys())
    print("Select a base color generation method, a starting color, or press [ENTER] to use defaults")
    while True:
        for i, option in enumerate(generation_options, 1):
            print(f"{i}. {option}")
        gen_choice = input("Enter your choice (1-3): ")
        if gen_choice == '1':
            print("Using random color generation")
            base=None
            weighted=False
            break
        if gen_choice == '2':
            print("Using weighted color generation")
            base=None
            weighted=True
            break
        if gen_choice == '3':
            print("Using a specific color")
            while True:
                hex_color = input("Enter your chosen color in hexadecimal (ex, '91ceca'): ")
                if len(hex_color) == 7: hex_color = hex_color[1:] # Remove # if included
                if len(hex_color) == 6:
                    try: 
                        r,g,b = [int(i,16) for i in [hex_color[2*i:2*i+2] for i in range(3)]] # Gross one liner to convert to 0-255
                        if min(r,g,b) > 0 and max(r,g,b) < 255:
                            base = hsl.RGB_to_HSL((r,g,b))
                            weighted=False
                            break
                        else:
                            print(f"Invalid hex color code (expected 0<R,G,B<255, got {r},{g},{b}")
                    except ValueError:
                        print("Invalid hex color code (not in hexadecimal)")
                else: print(f"Invalid hex color code (expected 6 characters, got {len(hex_color)})")
            print("Using base color:")
            base.preview()
            break
        if gen_choice == '':
            print("Using default (weighted generation)")
            base=None
            weighted=True
            break
        else:
            nr()
    
    print("\nSelect color scheme method press [ENTER] to use defaults")
    while True:
        for i, option in enumerate(palette_options,1):
            print(f"{i}. {option}")
        palette_choice = input("Enter your choice (1-3): ")
        if palette_choice == '1':
            print("Using random color scheme method")
            preferential=False
            scheme=None
            break
        if palette_choice == '2':
            print("Using pseudorandom (biased) color scheme method")
            preferential=True
            scheme=None
            break
        if palette_choice == '3':
            preferential=False
            print("\nSelect specific color scheme method")
            while True:
                for i, option in enumerate(scheme_options,1):
                    print(f"{i}. {option}")
                scheme_choice = input("Enter your choice: ")
                try:
                    int(scheme_choice)
                except ValueError:
                    nr()
                else:
                    if int(scheme_choice)-1 in range(len(scheme_options)):
                        scheme_choice = int(scheme_choice)
                        print(f"Using {scheme_options[scheme_choice-1]}")
                        scheme=scheme_options[scheme_choice-1]
                        break
                    else:
                        print("Choice is outside of range")
            break
        if palette_choice == '':
            print("Using default (pseudorandom)")
            preferential=True
            scheme=None
            break
        else:
            nr()
    print("\nSelect palette generation method or press [ENTER] to use defaults")
    while True:
        for i, option in enumerate(perfect_options, 1):
            print(f"{i}. {option}")
        perf_choice = input("Enter your choice (1-2): ")
        if perf_choice == '1':
            print("Using perfect palette generation")
            break
        if perf_choice == '2':
            print("Using imperfect palette generation")
            break
        if perf_choice == '':
            print("Using default (imperfect palette generation)")
            break
        else:
            nr()
    print("\nSelect number of colors in palette or press [ENTER] to use defaults")
    while True:
        num_colors = input("# of colors: ")
        if is_integer(num_colors):
            print(f"Using {num_colors} colors")
            N = int(num_colors)
            break
        if num_colors == '':
            print("Using default (5 colors)")
            N = 5
            break
        else:
            nr()

# Palette generation
print("\nGenerating palette:")
palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
while True:
    palette_colors = palette.all_colors()
    for i in palette_colors: i.preview()
    print("\nHappy with palette?")
    print("Hit [ENTER] or respond 'y' if yes, respond 'n' to regenerate with the same settings")
    print("Respond 'choose' to select a new base color from this palette")
    happy = input("Happy?: ")
    if happy.lower() == 'y' or happy == '':
        print("Continuing")
        break
    if happy.lower() == 'n':
        print("\nRegenerating palette:")
        palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
    if happy.lower() == 'choose' or happy.lower() == 'c':
        print("\nWhich color should be the new base?")
        for i in range(len(palette_colors)):
            print(str(i+1)+". "+palette_colors[i].preview(as_string=True))
        while True:
            color_choice = input("New base #: ")
            try:
                int(color_choice)
            except ValueError:
                nr()
            else:
                if int(color_choice)-1 in range(len(palette_colors)):
                    color_choice = int(color_choice)
                    print(f"\nNew palette using #{color_choice}:")
                    base = palette_colors[color_choice-1]
                    palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
                    break
                else:
                    print("Choice is outside of range")

    if happy.lower() != 'y' and happy.lower() != 'n' and happy.lower() != 'choose' and happy != '':
        nr()
        print()

print("\nPress [ENTER] or respond 'y' to continue to terminal generation or respond 'n' to exit")
while True:
    term_generation = input("Continue to terminal generation? ")
    if term_generation.lower() == 'y' or term_generation == '':
        print("Continuing to terminal generation")
        break
    if term_generation.lower() == 'n':
        quit()
    else:
        nr()

term_options = ['Basic', 'Similar hues']
term_generate = {
        '1' : lambda c: term.basic_term_colors(c),
        '2' : lambda c: term.colored_term_colors(c)
        }
print("\nSelect terminal color method or press [ENTER] to use default")
while True:
    for i, option in enumerate(term_options,1):
        print(f"{i}. {option}")
    term_choice = input("Enter your choice (1-2): ")
    if term_choice  == '1':
        print("Using basic")
        break
    if term_choice == '2':
        print("Using similar hues")
        break
    if term_choice == '':
        print("Using default (similar hues)")
        term_choice ='2'
        break
    else:
        nr()
terminal = term_generate[term_choice](palette.base_color)
print("\nGenerating complete theme:")
theme = thm.theme(palette,terminal)
while True:
    theme.preview(term_verbose=False)
    print("Happy with theme?")
    print("Hit [ENTER] or respond 'y' if yes, respond 'n' to regenerate with the same settings")
    print("Respond 'choose' to select a new base color from this theme")
    happy = input("Happy?: ")
    if happy.lower() == 'y' or happy == '':
        print("Continuing to save theme")
        break
    if happy.lower() == 'choose' or happy.lower() == 'c':
        print("\nWhich color should be the new base?")
        print("1. A color from the palette")
        print("2. A color from the terminal")
        print("3. A color from the dark theme terminal")
        base_from = input("Where from? ")
        if base_from == '1':
            for i in range(len(palette_colors)):
                print(str(i+1)+". "+palette_colors[i].preview(as_string=True))
            while True:
                color_choice = input("New base #: ")
                try:
                    int(color_choice)
                except ValueError:
                    nr()
                else:
                    if int(color_choice)-1 in range(len(palette_colors)):
                        color_choice = int(color_choice)
                        print(f"\nNew theme using #{color_choice}:")
                        base = palette_colors[color_choice-1]
                        palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
                        terminal = term_generate[term_choice](palette.base_color)
                        theme = thm.theme(palette,terminal)
                        break
                    else:
                        print("Choice is outside of range")
        if base_from == '2':
            all_term_colors = [theme.terminal.bg]+[theme.terminal.fg]+theme.terminal.normal_colors+theme.terminal.bright_colors
            for i in range(len(all_term_colors)):
                print(str(i+1)+". "+(" "*(i<9))+all_term_colors[i].preview(as_string=True))
            while True:
                color_choice = input("New base #: ")
                try:
                    int(color_choice)
                except ValueError:
                    nr()
                else:
                    if int(color_choice)-1 in range(len(all_term_colors)):
                        color_choice = int(color_choice)
                        print(f"\nNew theme using #{color_choice}:")
                        base = all_term_colors[color_choice-1]
                        palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
                        terminal = term_generate[term_choice](palette.base_color)
                        theme = thm.theme(palette,terminal)
                        break
                    else:
                        print("Choice is outside of range")
        if base_from == '3':
            all_term_colors = [theme.dark_terminal.bg]+[theme.dark_terminal.fg]+theme.dark_terminal.normal_colors+theme.dark_terminal.bright_colors
            for i in range(len(all_term_colors)):
                print(str(i+1)+". "+all_term_colors[i].preview(as_string=True))
            while True:
                color_choice = input("New base #: ")
                try:
                    int(color_choice)
                except ValueError:
                    nr()
                else:
                    if int(color_choice)-1 in range(len(all_term_colors)):
                        color_choice = int(color_choice)
                        print(f"\nNew theme using #{color_choice}:")
                        base = all_term_colors[color_choice-1]
                        palette = pal.N_palette(N=N,base=base,scheme=scheme,weighted=weighted,preferential=preferential)
                        terminal = term_generate[term_choice](palette.base_color)
                        theme = thm.theme(palette,terminal)
                        break
                    else:
                        print("Choice is outside of range")
    if happy.lower() == 'n':
        print("\nRegenerating theme:")
        palette = pal.N_palette(N=N,base=palette.base_color,scheme=scheme,weighted=weighted,preferential=preferential)
        terminal = term_generate[term_choice](palette.base_color)
        theme = thm.theme(palette,terminal)
    if happy.lower() != 'y' and happy.lower() != 'n' and happy.lower() != 'choose' and happy != '':
        nr()
        print()

print("\nPress [ENTER] or respond 'y' to continue to .json export or respond 'n' to exit")
while True:
    term_generation = input("Continue to export? ")
    if term_generation.lower() == 'y' or term_generation == '':
        print("Continuing to export")
        break
    if term_generation.lower() == 'n':
        quit()
    else:
        nr()

print("\nWhat should the file name be ('.json' automatically appended)?")
json_name = input("Name of json: ") 
theme.save_to_json(filename=json_name)
print(f"File exported as {json_name}.json. Full theme:")
theme.preview()
