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
#Hc     = Hw                    # Height


####    Areas
A_Composite_Ct  = tc*Hw
A_Composite_St  = 2*(Bf*tf + tw*Hw)
A_IShaped       = 2* Bf*tf + tw*Hw

#       Element Length
L               = 10 *ft

#=============================================================================
#    Loading
#=============================================================================

Py              = -100 *kip
























