exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())

import sys
#=============================================================================
#    Steel Parameters:
#=============================================================================
## Steel Material No. 1
b1          = 0.15
Es1         = 29000 *ksi
# Es1         = 10**10 #sys.maxsize
Fy1         = 50 *ksi
Esh1        = Es1/30
Fu1         = 65 *ksi
epsy1       = Fy1/Es1
eps_sh1     = 10 * epsy1
eps_ult1    = 0.15
# lsr1      = (20 *cm)/(1*cm) # lsr = Lu/db
lsr1        = 16.
beta1       = 1.0
r1          = 0.4
gamma1      = 0.5
alpha1      = 0.47
Cf1         = 0.21
Cd1         = 0.0
a1_1        = 4.3
limit1      = 0.01
R1_1        = 0.333
R2_1        = 18.0
R3_1        = 4.0

## Steel Material No. 2
b2          = b1      
Es2         = Es1     
Fy2         = Fy1     
Esh2        = Esh1    
Fu2         = Fu1     
epsy2       = epsy1   
eps_sh2     = eps_sh1 
eps_ult2    = eps_ult1
# lsr2      = (20 *cm)/(1*cm) # lsr = Lu/db
lsr2        = 16.
beta2       = 1.0
r2          = 0.4
gamma2      = 0.5
alpha2      = 0.47
Cf2         = 0.21
Cd2         = 0.0
a1_2        = 4.3
limit2      = 0.01
R1_2        = 0.333
R2_2        = 18.0
R3_2        = 4.0

#=============================================================================
#    Concrete Parameters:
#=============================================================================
# Unconfined Concrete
fpc1        = -4 *ksi
# Ec1       = 4700*abs(fpc)**0.5s               # For fpc in MPa
# Ec1       = 57000*abs(fpc)**0.5               # For fpc in psi
Ec1         = (57000*abs(fpc1*1000)**0.5)/1000   # For fpc in ksi
# Ec1       = 4840 *ksi
fpcu1       = 0.1 *fpc1
epsc01      = 2*fpc1/Ec1
epsU1       = -0.025
lam1        = 0.1
ft1         = 0.4 *ksi
Ets1        = 200 *ksi

# Confined Concrete
fpc2        = -4 *ksi
# Ec2       = 4700*abs(fpc)**0.5s               # For fpc in MPa
# Ec2       = 57000*abs(fpc)**0.5               # For fpc in psi
Ec2         = (57000*abs(fpc2*1000)**0.5)/1000   # For fpc in ksi
# Ec2       = 4840 *ksi
fpcu2       = 0.1 *fpc2
epsc02      = 2*fpc2/Ec2
epsU2       = -0.025
lam2        = 0.1
ft2         = 0.4 *ksi
Ets2        = 200 *ksi






















