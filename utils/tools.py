from math import floor
# This will come in handy
from dataclasses import dataclass
@dataclass
class HSL:
    h: float
    s: float
    l: float

    def __post_init__(self):
        # Correct H value (since we may go beyond 360)
        self.h = self.h%360
        if not (0<=self.s<=1):
            raise ValueError(f"Expected 0<S<1, got {self.s}")
        if not (0<=self.l<=1):
            raise ValueError(f"Expected 0<L<1, got {self.l}")
    
    # Class Functions
    def to_RGB(self):
        # Why is this so complicated though
        C= (1-abs(2*self.l-1))*self.s
        Hp = self.h/60
        X = C * (1-abs(Hp%2-1))
        m = self.l-C/2
        match floor(Hp):
            case 0:
                r,g,b = (C,X,0)
            case 1:
                r,g,b = (X,C,0)
            case 2:
                r,g,b = (0,C,X)
            case 3:
                r,g,b = (0,X,C)
            case 4:
                r,g,b = (X,0,C)
            case 5 | 6:
                r,g,b = (C,0,X)
        return (r+m, g+m, b+m) 


#RGB to HSL
def RGB_to_HSL(rgb:tuple):
    R, G, B = rgb
    # Check
    if R<0 or R>255 or G<0 or G>255 or B<0 or B>255:
        print("Invalid RGB. Expected 0<R,G,B<255, got: ", R, ",", G, ",", B)
        return
    R,G,B = R/255,G/255,B/255
    # Why so complex
    Cmax = max(R,G,B)
    Cmin = min(R,G,B)
    delta = Cmax-Cmin
    H_actions = {
            R: lambda:  60*(((G-B)/delta)%6),
            G: lambda:  60*((B-R)/delta+2),
            B: lambda:  60*((R-G)/delta+4)
            }
    if delta == 0: H = 0
    else: H = H_actions.get(Cmax, lambda: None)()
    L = (Cmax+Cmin)/2
    if delta == 0:
        S = 0
    else:
        S = delta/(1-abs(2*L-1))
    return (H,S,L)
            r,g,b = (X,C,0)
        case 2:
            r,g,b = (0,C,X)
        case 3:
            r,g,b = (0,X,C)
        case 4:
            r,g,b = (X,0,C)
        case 5 | 6:
            r,g,b = (C,0,X)
    return (r+m, g+m, b+m) 

# Nudge colors

