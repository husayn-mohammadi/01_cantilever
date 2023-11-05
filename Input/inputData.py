"C-PSW/CF Section: Shafaei PP=136"
# import sys
# from functions.ClassComposite import compo
exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
# exec(open("../Input/unitsSI.py").read()) # It SHOULD read and execute exec(open("Input/units    .py").read())
# exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())
#=============================================================================
#    Frame Data:
#=============================================================================
n_story         = 1
H_first         = 4.  *m
H_typical       = 3.5 *m
L_Bay           = 5  *m
H_story_List    = [H_first, *((n_story-1)*[H_typical])]       # [Hstory1, *((numStories-1)*[HstoryTypical])]
L_Bay_List      = 2*[L_Bay]#, 5.*m, 5.*m, 5.*m]        # [*LBays]

#=============================================================================
#    Elements
#=============================================================================
#       Element Length
L               = 108 *inch

# section={}
# #       Sections
# section = {
#     'wall': { # C-PSW/CF Wall Section
#         'tagSec': 1,
#         'tagInt': 1,
#         'Bf': 11*inch,
#         'tf': 3/16*inch,
#         'tw': 3/16*inch,
#         'Hw': 36*inch,
#         'tc': 9*inch,
#     },
#     'beam': { # Composite Beam Section
#         'tagSec': 2,
#         'tagInt': 2,
#         'Bf': 11*inch,
#         'tf': 3/16*inch,
#         'tw': 3/16*inch,
#         'Hw': 0.24 *m,
#         'tc': 9*inch,
#     }
# }

# for typeSection in section:
#     section[typeSection]['Hc2'] = (section[typeSection]['tc'] + 2*section[typeSection]['tw'])/2     # Height of   confined concrete i.e. Region 2 in documentation # Masoumeh Asgharpoor
#     section[typeSection]['Hc1'] = section[typeSection]['Hw'] - 2*section[typeSection]['Hc2']        # Height of unconfined concrete i.e. Region 1 in documentation
#     if section[typeSection]['Hc1'] < 0:
#         print(f"Hw is {section[typeSection]['Hw']}, but it cannot be less than {section[typeSection]['tc'] + 2*section[typeSection]['tw']}"); sys.exit()
    
#     section[typeSection]['A_Composite_St1'] = 2*(section[typeSection]['tw']*section[typeSection]['Hw'])
#     section[typeSection]['A_Composite_St2'] = 2*(section[typeSection]['Bf']*section[typeSection]['tf'])
#     section[typeSection]['A_Composite_Ct1'] = section[typeSection]['tc']*section[typeSection]['Hc1']
#     section[typeSection]['A_Composite_Ct2'] = section[typeSection]['tc']*section[typeSection]['Hc2']*2
    
#     section[typeSection]['As'] = section[typeSection]['A_Composite_St1'] + section[typeSection]['A_Composite_St2']
#     section[typeSection]['Ac'] = section[typeSection]['A_Composite_Ct1'] + section[typeSection]['A_Composite_Ct2']
    
#     section[typeSection]['I_Flanges'] = (1/12 * section[typeSection]['Bf'] * (section[typeSection]['Hw'] + section[typeSection]['tf'])**3) - (1/12 * section[typeSection]['Bf'] * section[typeSection]['Hw']**3)
#     section[typeSection]['I_Webs'] = 1/12 * (2*section[typeSection]['tw']) * section[typeSection]['Hw']**3
#     section[typeSection]['I_UnconfConc'] = 1/12 * section[typeSection]['tc'] * section[typeSection]['Hc1'] **3
#     section[typeSection]['I_ConfConc'] = 1/12 * section[typeSection]['tc'] * section[typeSection]['Hw']**3 - section[typeSection]['I_UnconfConc']
    
#     section[typeSection]['Is'] = section[typeSection]['I_Flanges'] + section[typeSection]['I_Webs']
#     section[typeSection]['Ic_uncracked'] = section[typeSection]['I_UnconfConc'] + section[typeSection]['I_ConfConc']

Hw          = 36*inch
lsr         = 48.
b           = 114*mm
NfibeY      = 3

Section = {}
Section = {
    'wall': { # C-PSW/CF Wall Section
        #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
        'tags'      : [1,      1,              2,           3,              4           ],
        #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
        'propWeb'   : [3/16*inch, Hw,        200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        'propFlange': [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        #propCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
        'propCore'  : [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]
    },
    'beam': { # Composite Beam Section
        #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
        'tags'      : [2,      5,              6,           7,              8           ],
        #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
        'propWeb'   : [3/16*inch, 0.4  *m,   200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        'propFlange': [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01],
        #propCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
        'propCore'  : [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]
    },
    }


# #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
# tags        = [1,      1,              2,           3,              4           ]
# #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
# propWeb     = [3/16*inch, 0.24 *m,   200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# propFlange  = [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# #propCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
# propCore    = [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]

#beam= compo(*tags, ALR, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
# beam = compo(*tags, 0.1, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)

# #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
# tags        = [2,      5,              6,           7,              8           ]
# #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
# propWeb     = [3/16*inch, 36*inch,   200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# propFlange  = [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# #propCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
# propCore    = [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]
#wall= compo(*tags, ALR, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
# wall = compo(*tags, 0.1, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)

#=============================================================================
#    Loading
#=============================================================================
#   Cantilever Loads
Py              = -3158 *kN
# or:
ALR             = 0.0  # Axial Load Ratio
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
load["wall"]    = 1.0*DL_Tributary + 0.25*LL_Tributary

##  Loading the Leaning Columns
n_Bay_x         = len(L_Bay_List)
A_SFRS          = (1.5 * L_Bay_y) * ((n_Bay_x+1) * L_Bay_x)
A_Leaning       = A_SFRS - A_Tributary*n_Bay_x
L_PWall         = L_Bay_y + ((n_Bay_x+1) * L_Bay_x) - n_Bay_x*Hw
DL_Leaning      = A_Leaning * DL_Floor + L_PWall*H_typical * DL_PWalls
LL_Leaning      = A_Leaning * LL_Floor
load["leaningColumn"] = 1.0*DL_Leaning + 0.25*LL_Leaning






















