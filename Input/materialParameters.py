import numpy as np

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
exec(open("MAIN.py").readlines()[19]) # It SHOULD read and execute exec(open("Input/inputData.py").read())

# These values and formulations are based on the paper "Nonlinear modeling for composite plate shear walls-concrete filled structures" by Masoumeh Asgarpoor (https://doi.org/10.1016/j.jobe.2022.105383)

# infinity = 10**10

ALR         = 0.0  # Axial Load Ratio

#=============================================================================
#    Concrete Parameters:
#=============================================================================
# Unconfined Concrete
fpc         = -4 *ksi
# Ec        = 4700*abs(fpc)**0.5s               # For fpc in MPa
# Ec        = 57000*abs(fpc)**0.5               # For fpc in psi
Ec          = (57000*abs(fpc*1000)**0.5)/1000   # For fpc in ksi
# Ec        = 4840 *ksi
epsc0       = 2*fpc/Ec
lam1        = 0.1
ft1         = 0.4 *ksi
Ets1        = 200 *ksi

# Confined Concrete
fpc2        = -4 *ksi
# Ec2       = 4700*abs(fpc)**0.5s               # For fpc in MPa
# Ec2       = 57000*abs(fpc)**0.5               # For fpc in psi
Ec2         = (57000*abs(fpc2*1000)**0.5)/1000   # For fpc in ksi
# Ec2       = 4840 *ksi
epsc02      = 2*fpc2/Ec2
lam2        = 0.1
ft2         = 0.4 *ksi
Ets2        = 200 *ksi

#=============================================================================
#    Steel Parameters:
#=============================================================================
## Steel Material No. 1
Es1         = 29000 *ksi
nu          = 0.28
Fy1         = 50 *ksi
Esh1        = Es1/30
Fu1         = 65 *ksi
epsy1       = Fy1/Es1
eps_sh1     = 10 * epsy1
eps_ult1    = 0.15

## Steel Material No. 2
Es2         = Es1     
Fy2         = Fy1     
Esh2        = Esh1    
Fu2         = Fu1     
epsy2       = epsy1   
eps_sh2     = eps_sh1 
eps_ult2    = eps_ult1

b           = 8 *inch  # minimum unsupported width of confined region in composite wall cross-section
lsr         = 16. # lsr = lu/db = 12**0.5 * lu/tw
beta        = 1.0
gamma       = 1.0
alpha       = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)
Cf          = 0.5
a1          = 4.3
limit       = 0.01
R1          = 0.333
R2          = 18.0
R3          = 4.0



#=============================================================================
#    Formulated Parameters:
#=============================================================================
Fy          = (Fy1 + Fy2)/2
Es          = (Es1 + Es2)/2
Fu          = (Fu1 + Fu2)/2
eps_sh      = (eps_sh1  + eps_sh2)/2
eps_ult     = (eps_ult1 + eps_ult2)/2

rhos        = (2*tw*Hw)/((2*tw + tc)*Hw) # Percentage of Steel

R           = b/tw * (12*(1-nu**2)/(4*np.pi))**0.5 * (Fy/Es)**0.5 # by Masoumeh Asgarpoor

frp         = -6.5*R*(fpc**1.46/Fy) + 0.12*fpc**1.03 # by Masoumeh Asgarpoor

fpcc        = fpc + 4*frp*(1+0.8*ALR)**3.5 # by Masoumeh Asgarpoor
Ecc         = (57000*abs(fpcc*1000)**0.5)/1000   # For fpc in ksi 
epscc0      = 2*fpcc/Ecc


fpcu        = 0.15 *fpc** 1.5  * Fy**0.01  * rhos**0.16    * (1-ALR)**(-0.5) * lsr**(-0.025) # by Masoumeh Asgarpoor 
if (fpcu/fpc < 0.45 or fpcu/fpc > 0.80):
    print("Warning!!! \n0.45 < fpcu/fpc < 0.80 is violated!!!")
    
fpccu       = 2.63 *fpcc**0.65 * Fy**0.001 * rhos**(-0.04) * (1-ALR)**( 0.4) * lsr**( 0.070) # by Masoumeh Asgarpoor 
if (fpccu/fpcc < 0.45 or fpccu/fpcc > 0.90):
    print("Warning!!! \n0.45 < fpccu/fpcc < 0.90 is violated!!!")

epscU       = 0.157   *epsc0 **(-0.67) * fpcu **0.23 *Fy**(-1.4) * rhos**0.06 * (1-ALR)**(-0.17) * lsr**0.12 # by Masoumeh Asgarpoor
if (epscU/epsc0 < 1.6 or epscU/epsc0 > 5.5):
    print("Warning!!! \n1.6 < epsccu/epscc < 5.5 is violated!!!")
    
epsccU      = 1.12e-6 *epscc0**(-0.33) * fpccu**0.83 *Fy**(0.77) * rhos**0.07 * (1-ALR)**( 0.15) * lsr**0.16 # by Masoumeh Asgarpoor 
if (epsccU/epscc0 < 4.0 or epsccU/epscc0 > 8.7):
    print("Warning!!! \n4.0 < epsccu/epscc < 8.7 is violated!!!")




r           = (15*lsr**0.37 * (Fy/fpc)**0.26 * eps_sh**0.3 * eps_ult**0.85)**-1 # by Masoumeh Asgarpoor 
if (r < 0.08 or r > 0.7):
    print("Warning!!! \n0.08 < r < 0.7 is violated!!!")
    
Cd          = 16 * (Fy/Fu)0.78 * eps_ult * (fpcu**0.5/fpc)**0.58 * r**0.37
if (Cd < 0.2 or Cd > 0.75):
    print("Warning!!! \n4.0 < epsccu/epscc < 8.7 is violated!!!")












