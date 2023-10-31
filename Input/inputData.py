"C-PSW/CF Section: Shafaei PP=136"

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
# exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())

#=============================================================================
#    Frame Data:
#=============================================================================
n               = 1
H_first         = 4.  *m
H_typical       = 3.5 *m
L_Bay           = 3  *m
H_story_List    = [H_first, *((n-1)*[H_typical])]       # [Hstory1, *((numStories-1)*[HstoryTypical])]
L_Bay_List      = 2*[L_Bay]#, 5.*m, 5.*m, 5.*m]        # [*LBays]

#=============================================================================
#    Elements
#=============================================================================
#       Element Length
L               = 108 *inch
NfibeY          = 3                        # Number of Fibers along Y-axis

section={}
#       Sections
section = {
    'wall': { # C-PSW/CF Wall Section
        'tagSec': 1,
        'tagInt': 1,
        'Bf': 11*inch,
        'tf': 3/16*inch,
        'tw': 3/16*inch,
        'Hw': 36*inch,
        'tc': 9*inch,
    },
    'beam': { # Composite Beam Section
        'tagSec': 2,
        'tagInt': 2,
        'Bf': 11*inch,
        'tf': 3/16*inch,
        'tw': 3/16*inch,
        'Hw': 16*inch,
        'tc': 9*inch,
    }
}

for typeSection in section:
    section[typeSection]['Hc2'] = (section[typeSection]['tc'] + 2*section[typeSection]['tw'])/2     # Height of   confined concrete i.e. Region 2 in documentation # Masoumeh Asgharpoor
    section[typeSection]['Hc1'] = section[typeSection]['Hw'] - 2*section[typeSection]['Hc2']        # Height of unconfined concrete i.e. Region 1 in documentation
    
    section[typeSection]['A_Composite_St1'] = 2*(section[typeSection]['tw']*section[typeSection]['Hw'])
    section[typeSection]['A_Composite_St2'] = 2*(section[typeSection]['Bf']*section[typeSection]['tf'])
    section[typeSection]['A_Composite_Ct1'] = section[typeSection]['tc']*section[typeSection]['Hc1']
    section[typeSection]['A_Composite_Ct2'] = section[typeSection]['tc']*section[typeSection]['Hc2']*2
    
    section[typeSection]['As'] = section[typeSection]['A_Composite_St1'] + section[typeSection]['A_Composite_St2']
    section[typeSection]['Ac'] = section[typeSection]['A_Composite_Ct1'] + section[typeSection]['A_Composite_Ct2']
    
    section[typeSection]['I_Flanges'] = (1/12 * section[typeSection]['Bf'] * (section[typeSection]['Hw'] + section[typeSection]['tf'])**3) - (1/12 * section[typeSection]['Bf'] * section[typeSection]['Hw']**3)
    section[typeSection]['I_Webs'] = 1/12 * (2*section[typeSection]['tw']) * section[typeSection]['Hw']**3
    section[typeSection]['I_UnconfConc'] = 1/12 * section[typeSection]['tc'] * section[typeSection]['Hc1'] **3
    section[typeSection]['I_ConfConc'] = 1/12 * section[typeSection]['tc'] * section[typeSection]['Hw']**3 - section[typeSection]['I_UnconfConc']
    
    section[typeSection]['Is'] = section[typeSection]['I_Flanges'] + section[typeSection]['I_Webs']
    section[typeSection]['Ic_uncracked'] = section[typeSection]['I_UnconfConc'] + section[typeSection]['I_ConfConc']


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
L_PWall         = L_Bay_y + ((n_Bay_x+1) * L_Bay_x) - n_Bay_x*section['wall']['Hw']
DL_Leaning      = A_Leaning * DL_Floor + L_PWall*H_typical * DL_PWalls
LL_Leaning      = A_Leaning * LL_Floor
load["leaningColumn"] = 1.0*DL_Leaning + 0.25*LL_Leaning




















