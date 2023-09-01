"Arbitrary Section: Shafaei PP=87"

# exec(open("functions/units.py").read())
exec(open("functions/unitsUS.py").read())

#=============================================================================
#    Elements
#=============================================================================

#       Sections:
##      Steel Sections:
###     Box Section:
H               = 20    *inch
tw              = 0.5   *inch
B               = 20    *inch
tf              = 0.5   *inch

A_Box           = H*B - (H-2*tf)*(B-2*tw)

###     Composite Section:

H_W             = 20    *inch
tw_W            = 0.5   *inch
B_W             = 20    *inch
tf_W            = 0.5   *inch

A_Composite_Ct     = (H_W-2*tf_W)*(B_W-2*tw_W)
A_Composite_St     = H_W*B_W - A_Composite_Ct


#       Element Length
# L               = 108 *inch
L               = 10 *ft

#=============================================================================
#    Loading
#=============================================================================



Py              = 100 *kip
# Py              = -0 *kN
























