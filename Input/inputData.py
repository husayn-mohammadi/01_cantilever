"C-PSW/CF Section: Shafaei PP=136"
# import sys
# from functions.ClassComposite import compo
exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
# exec(open("../Input/unitsSI.py").read()) # It SHOULD read and execute exec(open("Input/units    .py").read())
# exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())
#=============================================================================
#    Frame Data:
#=============================================================================
n_story         = 5
H_first         = 800 *mm
H_typical       = H_first #1000 *mm
L_Bay           = (600 + 300) *mm
H_story_List    = [H_first, *((n_story-1)*[H_typical])]       # [Hstory1, *((numStories-1)*[HstoryTypical])]
L_Bay_List      = 2*[L_Bay]#, 5.*m, 5.*m, 5.*m]        # [*LBays]

#=============================================================================
#    Elements
#=============================================================================
#       Element Length
L           = 10 *ft
tw = tf     = 5.9 *mm
Hw          = 600 *mm
bf          = 100 *mm
tc          = bf -2*tw
lsr         = 50.
b           = 114*mm
NfibeY      = 10

Section = {
    'wall': { # C-PSW/CF Wall Section
        #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
        'tags'      : [1,      1,              2,           3,              4           ],
        #propStPart = [B,      H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
        'propWeb'   : [tw,     Hw,        200*GPa, 372*MPa, 453*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        'propFlange': [bf,     tf,        200*GPa, 372*MPa, 453*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        #propCore   = [tc,     fpc,       wc,      lamConf, lamUnconf]
        'propCore'  : [tc,     58.7*MPa,  0.2*mm,  0.07,    0.2      ]
    },
    'beam': { # Composite Beam Section
        #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
        'tags'      : [2,      5,              6,           7,              8           ],
        #propStPart = [B,      H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
        'propWeb'   : [tw,     200 *mm,   200*GPa, 372*MPa, 453*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        'propFlange': [bf,     tf,        200*GPa, 372*MPa, 453*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        #propCore   = [tc,     fpc,       wc,      lamConf, lamUnconf]
        'propCore'  : [tc,     58.7*MPa,  0.2*mm,  0.07,    0.2      ]
    },
    }

#=============================================================================
#    Loading
#=============================================================================
#   Cantilever Loads
Py              = -3158 *kN
# or:
ALR             = 0.1  # Axial Load Ratio
#   Frame Loads
load={}
DL_Floor        = 90 *psf
DL_PWalls       = 25 *psf
LL_Floor        = 50 *psf
LL_Roof         = 20 *psf

##  Tributary Loading
L_Bay_y         = 4 *m
L_Bay_x         = L_Bay
A_Tributary     = 0.5*L_Bay_y * L_Bay_x
DL_Tributary    = A_Tributary * DL_Floor
LL_Tributary    = A_Tributary * LL_Floor
# load["wall"]    = 1.0*DL_Tributary + 0.25*LL_Tributary
load["wall"]    = 72 * kip

##  Loading the Leaning Columns
n_Bay_x         = len(L_Bay_List)
A_SFRS          = (1.5 * L_Bay_y) * ((n_Bay_x+1) * L_Bay_x)
A_Leaning       = A_SFRS - A_Tributary*n_Bay_x
L_PWall         = L_Bay_y + ((n_Bay_x+1) * L_Bay_x) - n_Bay_x*Hw
DL_Leaning      = A_Leaning * DL_Floor + L_PWall*H_typical * DL_PWalls
LL_Leaning      = A_Leaning * LL_Floor
# load["leaningColumn"] = 1.0*DL_Leaning + 0.25*LL_Leaning
load["leaningColumn"] = 1440 * kip






















