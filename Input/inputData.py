"C-PSW/CF Section: Shafaei PP=136"

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())
#=============================================================================
#    Elements
#=============================================================================

#       Sections
##      C-PSW/CF Wall Section
###     Flanges
Bf      = 11.   *inch           # Width
tf      = 0.19  *inch           # Height

###     Faceplates
tw      = 0.19  *inch           # Width
Hw      = 36.   *inch           # Height

###     Concrete Core
tc      = 9.    *inch           # Width
#Hc     = Hw                    # Height


####    Areas
A_Composite_Ct  = tc*Hw
A_Composite_St  = 2*(Bf*tf + tw*Hw)


#       Element Length
L               = 108 *inch

#=============================================================================
#    Loading
#=============================================================================

Py              = -210 *kip























