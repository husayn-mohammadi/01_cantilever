"C-PSW/CF Section: Shafaei PP=136"

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
# exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())

#=============================================================================
#    Loading
#=============================================================================

Py              = -934 *kN
# or:
ALR             = 0.02  # Axial Load Ratio

#=============================================================================
#    Elements
#=============================================================================

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


#       Element Length
L               = 108 *inch

























