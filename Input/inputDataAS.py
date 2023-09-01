"Arbitrary Section: Shafaei PP=87"

# exec(open("functions/units.py").read())
exec(open("functions/unitsUS.py").read())

#=============================================================================
#    Elements
#=============================================================================

#       Sections:
##      Steel Sections:
H               = 20    *inch
tw              = 0.5   *inch
B               = 20    *inch
tf              = 0.5   *inch

A_Composite_Ct  = (H-2*tf)*(B-2*tw)
A_Composite_St  = H*B - A_Composite_Ct
A_IShaped       = 2*B*tf + (H-2*tf)*tw


#       Element Length
L               = 10 *ft


#=============================================================================
#    Steel Parameters:
#=============================================================================
b       = 0.15
Es      = 29000 *ksi
Fy      = 50 *ksi
Esh     = Es/30
Fu      = 65 *ksi
epsy    = Fy/Es
eps_sh  = 10 * epsy
eps_ult = 0.15
# lsr     = (20 *cm)/(1*cm) # lsr = Lu/db
lsr     = 16.
beta    = 1.0
r       = 0.4
gamma   = 0.5
alpha   = 0.47
Cf      = 0.21
Cd      = 0.0
a1      = 4.3
limit   = 0.01
R1      = 0.333
R2      = 18.0
R3      = 4.0


#=============================================================================
#    Concrete Parameters:
#=============================================================================
fpc     = -4 *ksi
# Ec      = 4700*abs(fpc)**0.5s               # For fpc in MPa
# Ec      = 57000*abs(fpc)**0.5               # For fpc in psi
Ec      = (57000*abs(fpc*1000)**0.5)/1000   # For fpc in ksi
# Ec      = 4840 *ksi
fpcu    = 1 *fpc
epsc0   = 2*fpc/Ec
epsU    = -0.025
lam     = 0.1
ft      = 0.4 *ksi
Ets     = 200 *ksi

#=============================================================================
#    Loading
#=============================================================================

Py              = 100 *kip
























