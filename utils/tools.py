from math import floor
# RGB to HSL
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
# HSL to RGB
def HSL_to_RGB(hsl:tuple):
    H, S, L = hsl
    # Check
    if H<0 or H>360:
        print("Invalid hue. Expected 0<H<360, got: ", H)
        return
    if S<0 or S>100:
        print("Invalid saturation. Expected 0<S<100, got: ", S)
        return
    if L<0 or L>100:
        print("Invalid lightness. Expected 0<L<100, got: ", L)
        return
    if S>1:
        print("Converting S from percentage")
        S = S/100
    if L>1:
        print("Converting L from percentage")
        L = L/100
    # Why is this so complicated though
    C= (1-abs(2*L-1))*S
    Hp = H/60
    X = C * (1-abs(Hp%2-1))
    m = L-C/2
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

# Nudge colors

