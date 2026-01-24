from utils import hsl
from utils import palettes
from utils import term
from utils import theme
from generators import palette
import argparse

term_options = {
        'basic' : lambda c: term.basic_term_colors(c),
        'colored' : lambda c: term.colored_term_colors(c)
        }

def main(base,scheme,weighted,preferential,N,perfect,term):
    pal = palette.main(base=base,scheme=scheme,weighted=weighted,preferential=preferential,N=N,perfect=perfect)
    term = term_options[term](pal.base_color)
    thm = theme.theme(pal,term)
    return thm

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base", default=None, help="Base color to use (in hexadecimal)")
    parser.add_argument("-s", "--scheme", default=None, choices=["complementary","split_complementary","analogous","triadic","square","tetradic","monochromatic"],help="What scheme to use for palette generation")
    parser.add_argument("-w", "--weighted", type=bool, default=True, help="Colors weighted towards normal")
    parser.add_argument("-p", "--preferential", type=bool, default=True, help="Use a more 'conventional' scheme")
    parser.add_argument("-i", "--imperfect", type=bool, default=True, help="Shift palettes slightly off a perfect construction")
    parser.add_argument("-n", "--num", type=int, default=5, help="How many colors in the palette")
    parser.add_argument("-t", "--term", default='colored', choices=["basic","colored"], help="What terminal color generation method to use")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    thm = main(base=args.base,scheme=args.scheme,weighted=args.weighted,preferential=args.preferential,N=args.num,perfect=(not args.imperfect), term=args.term)
    thm.preview()
