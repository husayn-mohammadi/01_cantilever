"Arbitrary Section: Shafaei PP=87"

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())
#=============================================================================
#    Elements
#=============================================================================

#       Sections
##      Steel Sections
###     Flanges
Bf      = 20    *inch           # Width
tf      = 0.5   *inch           # Height

###     Faceplates
tw      = 0.5   *inch           # Width
Hw      = 19.5  *inch           # Height

###     Concrete Core
tc      = Bf - 2*tw             # Width
Hc1     = 20.   *inch           # Height of unconfined concrete i.e. Region 1 in documentation
Hc2     = (Hw - Hc1)/2          # Height of   confined concrete i.e. Region 2 in documentation


####    Areas
A_Composite_St1 = 2*(tw*Hw)     # St1 is used for Faceplates
A_Composite_St2 = 2*(Bf*tf)     # St2 is used for Flange Plates
A_Composite_Ct1 = tc*Hc1        # Ct1 (unconfined) is used for middle concrete
A_Composite_Ct2 = tc*Hc2*2      # Ct2   (confined) is used for boundary elements

A_IShaped       = 2* Bf*tf + tw*Hw

#       Element Length
L               = 10 *ft

#=============================================================================
#    Loading
#=============================================================================

Py              = -100 *kip
























