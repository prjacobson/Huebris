from utils import hsl
from utils import palettes
import argparse

def main(base,scheme,weighted,preferential,N,perfect):
    if base is not None:
        if len(base) == 7: base = base[1:] # Remove # if included
        if len(base) == 6:
            try:
                r,g,b = [int(i,16) for i in [base[2*i:2*i+2] for i in range(3)]] # Gross one liner to convert to 0-255
                if min(r,g,b) > 0 and max(r,g,b) < 255:
                    base = hsl.RGB_to_HSL((r,g,b))
                else:
                    print("Invalid hex color code, using random base")
                    base = None
            except ValueError:
                print("Invalid hex color code, using random base")
                base = None
    return palettes.N_palette(base=base,scheme=scheme,weighted=weighted,preferential=preferential,N=N,perfect=perfect)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base", default=None, help="Base color to use (in hexadecimal)")
    parser.add_argument("-s", "--scheme", default=None, choices=["complementary","split_complementary","analogous","triadic","square","tetradic","monochromatic"],help="What scheme to use for palette generation")
    parser.add_argument("-w", "--weighted", type=bool, default=True, help="Colors weighted towards normal")
    parser.add_argument("-p", "--preferential", type=bool, default=True, help="Use a more 'conventional' scheme")
    parser.add_argument("-n", "--num", type=int, default=5, help="How many colors in the palette")
    parser.add_argument("-i", "--imperfect", type=bool, default=True, help="Shift palettes slightly off a perfect construction")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    pal = main(base=args.base,scheme=args.scheme,weighted=args.weighted,preferential=args.preferential,N=args.num,perfect=(not args.imperfect))
    pal.preview()
