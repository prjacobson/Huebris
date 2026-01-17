# Defines the hsl() class and things you can do to/with a color

from random import random
from random import gauss # For weighted color generation
from random import expovariate # See above
from math import floor
# This will come in handy
from dataclasses import dataclass
import utils.parameters as par

# Name some colors (ordered for terminal colors)
named_colors = {
        'red' : 0,
        'green': 120,
        'yellow': 60,
        'blue': 240,
        'magenta': 300,
        'cyan': 180
        }

# Define HSL class and functions
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
    def hexed(self):
        r,g,b = self.to_RGB()
        to_hex = lambda c : hex(floor(c/1))[2:].zfill(2)
        return to_hex(r)+to_hex(g)+to_hex(b)
    def preview(self, verbose=False):
        r,g,b = self.to_RGB()
        if verbose:
            r_h, r_s, r_l = round(self.h,3),round(self.s,3),round(self.l,3)
            print(f"\033[48;2;{r};{g};{b}m RGB: {r},{g},{b} HSL: {r_h},{r_s},{r_l} \033[0m")
        else:
            print(f"\033[48;2;{r};{g};{b}m RGB: #{self.hexed()} \033[0m")
    # Colorscheme options
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
        lightness_range = par.monochrome_range
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
    # expansion methods
    fudges = {
            'h' : lambda c,x: c.rotate(x),
            's' : lambda c,x: c.saturate(x),
            'l' : lambda c,x: c.lighten(x)
            }
    hue_fudge = par.hue_fudge
    min_hue_fudge = par.min_hue_fudge
    sat_fudge = par.sat_fudge
    min_sat_fudge = par.min_sat_fudge
    light_fudge = par.light_fudge
    min_light_fudge = par.min_light_fudge
    s_bound = par.s_bound
    l_bound = par.l_bound
    # unidirectional fudge
    def N_fudge(self,N=1,param='h'):
        if N==0:
            return []
        if param == 'h':
            dir = [-1,1][random()<=0.5]
            fudge_amount = self.min_hue_fudge+(random()*(self.hue_fudge-self.min_hue_fudge))
        # if close to bounds of S or L, don't fudge towards center
        # also don't fudge O.O.B.
        if param == 's':
            if self.s < self.s_bound: dir = 1
            elif self.s > 1-self.s_bound: dir = -1
            else: dir = [-1,1][random()<=0.5]
            if (self.s+dir*self.sat_fudge)<0 or (self.s+dir*self.sat_fudge)>1:
                fudge_amount = min((1-self.s),self.s)
            else: fudge_amount = self.sat_fudge
            fudge_amount = self.min_sat_fudge+(random()*(fudge_amount-self.min_sat_fudge))
        if param == 'l':
            if self.l < self.l_bound: dir = 1
            elif self.l > 1-self.l_bound: dir = -1
            else: dir = [-1,1][random()<=0.5]
            if (self.l+dir*self.light_fudge)<0 or (self.l+dir*self.light_fudge)>1:
                fudge_amount = min((1-self.l),self.l)
            else: fudge_amount = self.light_fudge
            fudge_amount = self.min_light_fudge+(random()*(fudge_amount-self.min_light_fudge))
        # Get fudged colors
        fudge_amount = fudge_amount/N
        colors = []
        for i in range(N):
            colors.append(self.fudges[param](self,fudge_amount*dir*(i+1)))
        return colors
    # symmetric fudge
    # If called close to an edge, instead fudge unidirectionally
    def sym_fudge(self,N=1,param='h'):
        if N==0:
            return []
        if param == 'h':
            fudge_amount = random()*self.hue_fudge
            fudge_amount = self.min_hue_fudge+(random()*(fudge_amount-self.min_hue_fudge))
        # don't fudge O.O.B.
        if param == 's':
            if self.s < self.s_bound or self.s > 1-self.s_bound:
                return self.N_fudge(2*N,param)
            if (self.s-self.sat_fudge)<0 or (self.s+self.sat_fudge)>1:
                fudge_amount = min((1-self.s),self.s)
            else: fudge_amount = self.sat_fudge
            fudge_amount = random()*fudge_amount
            fudge_amount = self.min_sat_fudge+(random()*(fudge_amount-self.min_sat_fudge))
        if param == 'l':
            if self.l < self.l_bound or self.l > 1-self.l_bound:
                return self.N_fudge(2*N,param)
            if (self.l-self.light_fudge)<0 or (self.l+self.light_fudge)>1:
                fudge_amount = min((1-self.l),self.l)
            else: fudge_amount = self.light_fudge
            fudge_amount = self.min_light_fudge+(random()*(fudge_amount-self.min_light_fudge))
        # Get fudged colors
        fudge_amount = fudge_amount/N
        colors = []
        for i in range(N):
            colors.append(self.fudges[param](self,fudge_amount*-(i+1)))
            colors.append(self.fudges[param](self,fudge_amount*(i+1)))
        return colors
    # Get closest named color
    def get_name(self):
        match(self.h):
            case _ if self.h<30 or self.h>=330:
                return 'red'
            case _ if 30<=self.h<90:
                return 'yellow'
            case _ if 90<=self.h<150:
                return 'green'
            case _ if 150<=self.h<210:
                return 'cyan'
            case _ if 210<=self.h<270:
                return 'blue'
            case _ if 270<=self.h<330:
                return 'magenta'
    def get_named_color_distance(self,name):
        hue = self.h
        named_hue = named_colors[name]
        distance = min(abs(named_hue-hue),360-abs(named_hue-hue))
        return distance
    def get_named_color(self,color):
        start_color = self.get_name()
        color_list = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
        rotate_amt = ((color_list.index(color)-color_list.index(start_color))%6)*60
        return self.rotate(rotate_amt)
    # Calculate relative luminance
    def relative_luminance(self):
        r,g,b = self.to_RGB()
        # sRGB space
        Rs,Gs,Bs = r/255,g/255,b/255
        # Get R G B for luminance calculation
        if Rs <= 0.03928: Rl = Rs/12.92
        else: Rl = ((Rs+0.055)/1.055)**2.4
        if Gs <= 0.03928: Gl = Gs/12.92
        else: Gl = ((Gs+0.055)/1.055)**2.4
        if Bs <= 0.03928: Bl = Bs/12.92
        else: Bl = ((Bs+0.055)/1.055)**2.4
        L = 0.2126*Rl + 0.7152*Gl + 0.0722*Bl
        return L

# Generators
def random_HSL():
    return HSL(random()*360,random(),random())
def weighted_HSL():
    saturation_mean = par.saturation_mean
    lightness_mean = par.lightness_mean
    lightness_var = par.lightness_var
    saturation = -1
    lightness = -1
    while saturation<0 or 1<saturation:
        saturation = 1-expovariate(1/(1-saturation_mean))
    while lightness<0 or 1<lightness:
        lightness = gauss(lightness_mean,lightness_var)
    return HSL(random()*360,saturation,lightness)

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

# Contrast ratio
def contrast_ratio(c1:HSL,c2:HSL):
    L1 = c1.relative_luminance()
    L2 = c2.relative_luminance()
    lighter = max(L1,L2)
    darker = min(L1,L2)
    return (lighter+0.05)/(darker+0.05)
