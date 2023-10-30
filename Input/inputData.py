"C-PSW/CF Section: Shafaei PP=136"

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
# exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())

#=============================================================================
#    Frame Data:
#=============================================================================
n               = 3
H_first         = 4.  *m
H_typical       = 3.5 *m
L_Bay           = 6.  *m
H_story_List    = [H_first, *((n-1)*[H_typical])]       # [Hstory1, *((numStories-1)*[HstoryTypical])]
L_Bay_List      = 2*[L_Bay]#, 5.*m, 5.*m, 5.*m]        # [*LBays]

#=============================================================================
#    Elements
#=============================================================================
#       Element Length
L               = 108 *inch

#       Sections
##      C-PSW/CF Wall Section
###     Flanges
Bf      = 11.   *inch           # Width
tf      = 3/16  *inch           # Height

###     Faceplates
tw      = 3/16  *inch           # Width
Hw      = 36.   *inch           # Height

###     Concrete Core
tc      = 9.    *inch           # Width
Hc2     = (tc + 2*tw)/2         # Height of   confined concrete i.e. Region 2 in documentation # Masoumeh Asgharpoor
Hc1     = Hw - 2*Hc2            # Height of unconfined concrete i.e. Region 1 in documentation


####    Areas
A_Composite_St1 = 2*(tw*Hw)     # St1 is used for Faceplates
A_Composite_St2 = 2*(Bf*tf)     # St2 is used for Flange Plates
A_Composite_Ct1 = tc*Hc1        # Ct1 (unconfined) is used for middle concrete
A_Composite_Ct2 = tc*Hc2*2      # Ct2   (confined) is used for boundary elements

As              = A_Composite_St1 + A_Composite_St2
Ac              = A_Composite_Ct1 + A_Composite_Ct2

####    Moment of Inertia
I_Flanges       = (1/12 * Bf * (Hw + tf)**3) - (1/12 * Bf * Hw**3)
I_Webs          = 1/12 * (2*tw) * Hw**3
I_UnconfConc    = 1/12 * tc * Hc1**3
I_ConfConc      = 1/12 * tc * Hw**3 - I_UnconfConc

Is              = I_Flanges + I_Webs
Ic_uncracked    = I_UnconfConc + I_ConfConc



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
load["wall"]    = 1.0*DL_Tributary + 0.25*LL_Tributary

##  Loading the Leaning Columns
n_Bay_x         = len(L_Bay_List)
A_SFRS          = (1.5 * L_Bay_y) * ((n_Bay_x+1) * L_Bay_x)
A_Leaning       = A_SFRS - A_Tributary*n_Bay_x
L_PWall         = L_Bay_y + ((n_Bay_x+1) * L_Bay_x) - n_Bay_x*Hw
DL_Leaning      = A_Leaning * DL_Floor + L_PWall*H_typical * DL_PWalls
LL_Leaning      = A_Leaning * LL_Floor
load["leaningColumn"] = 1.0*DL_Leaning + 0.25*LL_Leaning




















