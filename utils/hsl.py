from random import random
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
    def rotate(self,degrees) -> "HSL":
        return HSL((self.h + degrees),self.s,self.l)
    def lighten(self,amount) -> "HSL":
        return HSL(self.h,self.s,self.l+amount)
    def saturate(self,amount) -> "HSL":
        return HSL(self.h,self.s+amount,self.l)
    def to_RGB(self) -> "RGB Tuple":
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
        return (round((r+m)*255), round((g+m)*255), round((b+m)*255)) 
    # Preview color
    def preview(self):
        r,g,b = self.to_RGB()
        print(f"\033[48;2;{r};{g};{b}m RGB: {r},{g},{b} HSL: {self.h},{self.s},{self.l} \033[0m")
    # Color options
    def complementary(self) -> "HSL":
        return self.rotate(180)
    def split_complementary(self):
        color_1 = self.rotate(180-30)
        color_2 = self.rotate(180+30)
        return color_1,color_2
    def analogous(self):
        color_1 = self.rotate(-30)
        color_2 = self.rotate(30)
        return color_1, color_2
    def triadic(self):
        color_1 = self.rotate(-120)
        color_2 = self.rotate(120)
        return color_1, color_2
    def square(self):
        color_1 = self.rotate(-90)
        color_2 = self.rotate(90)
        color_3 = self.rotate(180)
        return color_1, color_2, color_3
    def tetradic(self):
        # Could go both directions
        pm = [-1,1][random()<=0.5]
        color_1 = self.rotate(pm*60)
        color_2 = self.rotate(180)
        color_3 = self.rotate(180+pm*60)
        return color_1, color_2, color_3
    def monochromatic(self,count=4):
        # count is how many additional colors
        # count=4 => base + 4 k
        colors = []
        # Set range
        lightness_range = 0.25
        lightness_step = lightness_range/(count+1)
        # Take appropriate steps
        if (self.l-(count/2)*lightness_step) < 0:
            for i in range(count):
                colors.append(self.lighten((i+1)*lightness_step))
            return tuple(colors)
        elif (self.l+(count/2)*lightness_step) > 1:
            for i in range(count):
                colors.append(self.lighten(-(i+1)*lightness_step))
            return tuple(colors)
        else:
            halved = floor(count/2)
            # choose which side gets extra
            if count%2 != 0:
                extra = [random()<=0.5]
                extra.append(not extra[0])
            else:
                extra=[0,0]
            #darken
            for i in range(halved+extra[0]):
                colors.append(self.lighten(-(i+1)*lightness_step))
            #lighten
            for i in range(halved+extra[1]):
                colors.append(self.lighten((i+1)*lightness_step))
            return tuple(colors)

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
    return HSL(H,S,L)


