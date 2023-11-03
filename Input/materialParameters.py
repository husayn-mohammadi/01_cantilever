import numpy as np

exec(open("MAIN.py").readlines()[18])               # It SHOULD read and execute exec(open(f"Input/unitsSI.py").read())
exec(open("MAIN.py").readlines()[19])               # It SHOULD read and execute exec(open("Input/inputData.py").read())
exec(open("Input/inputData.py").readlines()[9])     # It SHOULD read and execute ALR = 0.0  # Axial Load Ratio

global definedMatListglobal; definedMatList=[]
# exec(open("unitsSI.py").read())
# exec(open("inputData.py").read())

# These values and formulations are based on the paper "Nonlinear modeling for composite plate shear walls-concrete filled structures" by Masoumeh Asgarpoor (https://doi.org/10.1016/j.jobe.2022.105383)

# infinity = 10**10

#=============================================================================
#    Concrete Parameters:
#=============================================================================

# fpc         = 50.9 *MPa                                             # Masoumeh Asgharpoor: scope of study 32.5<fpc<102 (MPa)
# print(f"fpc\t\t= {fpc/MPa:.2f} MPa")
# Ec        = 4700*abs(fpc/MPa)**0.5s                               # With fpc in MPa  ==> ACI 318 - 2019 SI
# Ec        = 57000*abs(fpc)**0.5                                   # With fpc in psi  ==> ACI 318 - 2019 US
# Ec        = (57000*abs(fpc*1000)**0.5)/1000                       # With fpc in ksi  ==> ACI 318 - 2019 US
# Ec          = (21.5e3*MPa * 1.0 * (abs(fpc/MPa)/10)**(1/3))         # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
# Ec        = 4840 *ksi
# print(f"Ec\t\t= {Ec/MPa:.2f} MPa")
# epsc0       = 2*fpc/Ec
# print(f"epsc0\t= {epsc0:.5f}")
# lam1        = 0.25                                                   # Unconfined Concrete
# lam2        = 0.05                                                   # Confined Concrete
# fts         = 1.0*(0.3 * (fpc/MPa - 8)**(2/3))*MPa                   # CEB-FIB-2010 Eq. (5.1-5)
# print(f"fts\t\t= {fts/MPa:.2f} MPa")
# wc          = 0.2 *mm                                               # Crack width (Average of 0.15 to  0.25 mm)
# Gf          = (73 * (fpc/MPa)**0.18)                                # Fracture Energy CEB-FIB-2010 section 5.1.5.2
# Ets         = abs(1/(1-(2*Ec*Gf)/(wc*fts**2)))*Ec                   # Article: THE INFLUENCE OF AGGREGATE SIZE ON THE WIDTH OF FRACTURE PROCESS ZONE IN CONCRETE MEMBERS

# print(f"Ets\t\t= {Ets/MPa:.2f} MPa")

#       Concrete Usage Location
section['wall']['CtUnconfined']={}; section['wall']['CtConfined']={}

##1     Unconfined Concrete (Center) hereafter referred to as "unconfined"

section['wall']['CtUnconfined']['fpc']      = 50.9 *MPa
section['wall']['CtUnconfined']['lam']      = 0.25
section['wall']['CtUnconfined']['wc']       = 0.2 *mm                                               # Crack width (Average of 0.15 to  0.25 mm)

section['wall']['CtUnconfined']['Ec']       = (21.5e3*MPa * 1.0 * (abs(section['wall']['CtUnconfined']['fpc']/MPa)/10)**(1/3)) # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
section['wall']['CtUnconfined']['epsc0']    = 2*section['wall']['CtUnconfined']['fpc']/section['wall']['CtUnconfined']['Ec'] # Crack width (Average of 0.15 to  0.25 mm)
section['wall']['CtUnconfined']['Gf']       = (73 * (section['wall']['CtUnconfined']['fpc']/MPa)**0.18) # Fracture Energy CEB-FIB-2010 section 5.1.5.2
section['wall']['CtUnconfined']['fts']      = 1.0*(0.3 * (section['wall']['CtUnconfined']['fpc']/MPa - 8)**(2/3))*MPa # CEB-FIB-2010 Eq. (5.1-5)
section['wall']['CtUnconfined']['Ets']      = abs(1/(1-(2*section['wall']['CtUnconfined']['Ec']*section['wall']['CtUnconfined']['Gf'])/(section['wall']['CtUnconfined']['wc']*section['wall']['CtUnconfined']['fts']**2)))*section['wall']['CtUnconfined']['Ec']


#=============================================================================
#    Steel Parameters:
#=============================================================================
nu          = 0.28

## Steel Material No. 1 (For Webs of the Composite Walls)
# Es1         = 200   *GPa
# Fy1         = 422   *MPa
# Esh1        = Es1/30
# Fu1         = 473   *MPa
# epsy1       = Fy1/Es1
# eps_sh1     = 0.007
# eps_ult1    = 0.12
# alpha1      = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)

## Steel Material No. 2 (For Flanges of the Composite Walls)
# Es2         = Es1     
# Fy2         = Fy1     
# Esh2        = Esh1    
# Fu2         = Fu1     
# epsy2       = epsy1   
# eps_sh2     = eps_sh1 
# eps_ult2    = eps_ult1
# alpha2      = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)

section['wall']['StWeb']={}; section['wall']['StFlange']={}
##1     Web Steel
section['wall']['StWeb']['Es']          = 200   *GPa
section['wall']['StWeb']['Fy']          = 422   *MPa
section['wall']['StWeb']['Esh']         = section['wall']['StWeb']['Es']/30
section['wall']['StWeb']['Fu']          = 473   *MPa
section['wall']['StWeb']['epsy']        = section['wall']['StWeb']['Fy']/section['wall']['StWeb']['Es']
section['wall']['StWeb']['eps_sh']      = 0.007
section['wall']['StWeb']['eps_ult']     = 0.12
section['wall']['StWeb']['alpha']       = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)

##2     Flange Steel
section['wall']['StFlange']['Es']       = section['wall']['StWeb']['Es']     
section['wall']['StFlange']['Fy']       = section['wall']['StWeb']['Fy']     
section['wall']['StFlange']['Esh']      = section['wall']['StWeb']['Esh']    
section['wall']['StFlange']['Fu']       = section['wall']['StWeb']['Fu']     
section['wall']['StFlange']['epsy']     = section['wall']['StWeb']['epsy']   
section['wall']['StFlange']['eps_sh']   = section['wall']['StWeb']['eps_sh'] 
section['wall']['StFlange']['eps_ult']  = section['wall']['StWeb']['eps_ult']
section['wall']['StFlange']['alpha']    = section['wall']['StWeb']['alpha']  


#=============================================================================
#    Formulated Parameters:
#=============================================================================
# Fy          = (Fy1 + Fy2)/2
# print(f"Fy\t\t= {Fy/MPa:.2f} MPa")
# Es          = (Es1 + Es2)/2
# print(f"Es\t\t= {Es/MPa:.2f} MPa")
# Fu          = (Fu1 + Fu2)/2
# print(f"Fu\t\t= {Fu/MPa:.2f} MPa")
# eps_sh      = (eps_sh1  + eps_sh2)/2
# print(f"eps_sh\t= {eps_sh:.5f}")
# eps_ult     = (eps_ult1 + eps_ult2)/2
# print(f"eps_ult\t= {eps_ult:.5f}")

Es          = (section['wall']['StFlange']['Es']        + section['wall']['StWeb']['Es']        )/2
Fy          = (section['wall']['StFlange']['Fy']        + section['wall']['StWeb']['Fy']        )/2
Fu          = (section['wall']['StFlange']['Fu']        + section['wall']['StWeb']['Fu']        )/2
eps_sh      = (section['wall']['StFlange']['eps_sh']    + section['wall']['StWeb']['eps_sh']    )/2
eps_ult     = (section['wall']['StFlange']['eps_ult']   + section['wall']['StWeb']['eps_ult']   )/2

beta        = 1.0
gamma       = 1.0
Cf          = 0.5
a1          = 4.3
limit       = 0.01
R1          = 0.333
R2          = 18.0
R3          = 4.0

section['wall']['b']                     = 114 *mm  # minimum unsupported width of confined region in composite wall cross-section
section['wall']['lsr']                   = 48. # lsr = lu/db = 12**0.5 * lu/tw
section['wall']['rhos']                  = (2*section['wall']['tw'])/(section['wall']['tc']) # Percentage of Steel
section['wall']['R']                     = section['wall']['b']/section['wall']['tw'] * (12*(1-nu**2)/(4*np.pi**2))**0.5 * (Fy/Es)**0.5 # Masoumeh Asgarpoor
section['wall']['frp']                   = (-6.5*section['wall']['R']*((section['wall']['CtUnconfined']['fpc']/MPa)**1.46/(Fy/MPa)) + 0.12*(section['wall']['CtUnconfined']['fpc']/MPa)**1.03)*MPa # Masoumeh Asgarpoor
section['wall']['CtConfined']['fpc']     = ((section['wall']['CtUnconfined']['fpc']/MPa) + 4*(section['wall']['frp']/MPa)*(1+0.8*ALR)**3.5)*MPa # Masoumeh Asgarpoor
section['wall']['CtConfined']['Ec']      = (21.5e3*MPa * 1.0 * (abs(section['wall']['CtConfined']['fpc']/MPa)/10)**(1/3)) # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
section['wall']['CtConfined']['epsc0']   = 2*section['wall']['CtConfined']['fpc']/section['wall']['CtConfined']['Ec']
section['wall']['CtUnconfined']['fpcu']  = (0.15 *(section['wall']['CtUnconfined']['fpc']/MPa)** 1.5  * (Fy/MPa)**0.01  * section['wall']['rhos']**0.16    * (1-ALR)**(-0.5) * section['wall']['lsr']**(-0.025))*MPa # Masoumeh Asgarpoor 
section['wall']['CtUnconfined']['epscU'] = 0.157   *section['wall']['CtUnconfined']['epsc0'] **(-0.67) * (section['wall']['CtUnconfined']['fpcu']/MPa) **0.23 *(Fy/MPa)**(-1.4) * section['wall']['rhos']**0.06 * (1-ALR)**(-0.17) * section['wall']['lsr']**0.12 #Masoumeh Asgarpoor
section['wall']['CtConfined']['fpcu']   = (2.63 *(section['wall']['CtConfined']['fpc']/MPa)**0.65 * (Fy/MPa)**0.001 * section['wall']['rhos']**(-0.04) * (1-ALR)**( 0.4) * section['wall']['lsr']**( 0.070))*MPa # Masoumeh Asgarpoor 
section['wall']['CtConfined']['epscU']  = 1.12e-6 *section['wall']['CtConfined']['epsc0']**(-0.33) * (section['wall']['CtConfined']['fpcu']/MPa)**0.83 *(Fy/MPa)**(0.77) * section['wall']['rhos']**0.07 * (1-ALR)**( 0.15) * section['wall']['lsr']**0.16 #Masoumeh Asgarpoor 
section['wall']['r']                     = (15*section['wall']['lsr']**0.37 * (Fy/section['wall']['CtUnconfined']['fpc'])**0.26 * eps_sh**0.3 * eps_ult**0.85)**-1 # Masoumeh Asgarpoor 
section['wall']['Cd']                    = 16 * (Fy/Fu)**0.78 * eps_ult * ((section['wall']['CtUnconfined']['fpcu']/MPa)**0.5/(section['wall']['CtUnconfined']['fpc']/MPa))**0.58 * section['wall']['r']**0.37 # Masoumeh Asgarpoor 

print(f"fpcc\t= {section['wall']['CtConfined']['fpc']/MPa:.2f} MPa")
print(f"Ecc\t\t= {section['wall']['CtConfined']['Ec']/MPa:.2f} MPa")
print(f"epscc0\t= {section['wall']['CtConfined']['epsc0']:.5f}")

print(f"fpcu\t= {section['wall']['CtUnconfined']['fpcu']/MPa:.2f} MPa")
if (section['wall']['CtUnconfined']['fpcu']/section['wall']['CtUnconfined']['fpc'] < 0.45):
    print(f"Warning!!! fpcu/fpc={section['wall']['CtUnconfined']['fpcu']/section['wall']['CtUnconfined']['fpc']:.2f} < 0.45")
if (section['wall']['CtUnconfined']['fpcu']/section['wall']['CtUnconfined']['fpc'] > 0.80):
    print(f"Warning!!! fpcu/fpc={section['wall']['CtUnconfined']['fpcu']/section['wall']['CtUnconfined']['fpc']:.2f} > 0.80")

print(f"epscU\t= {section['wall']['CtUnconfined']['epscU']:.5f}")
if (section['wall']['CtUnconfined']['epscU']/section['wall']['CtUnconfined']['epsc0'] < 1.6):
    print(f"Warning!!! epscU/epsc0={section['wall']['CtUnconfined']['epscU']/section['wall']['CtUnconfined']['epsc0']:.2f} < 1.6")
if (section['wall']['CtUnconfined']['epscU']/section['wall']['CtUnconfined']['epsc0'] > 5.5):
    print(f"Warning!!! epscU/epsc0={section['wall']['CtUnconfined']['epscU']/section['wall']['CtUnconfined']['epsc0']:.2f} > 5.5")

print(f"fpccu\t= {section['wall']['CtConfined']['fpcu']/MPa:.2f} MPa")
if (section['wall']['CtConfined']['fpcu']/section['wall']['CtConfined']['fpc'] < 0.45):
    print(f"Warning!!! fpccu/fpcc={section['wall']['CtConfined']['fpcu']/section['wall']['CtConfined']['fpc']:.2f} < 0.45")
if (section['wall']['CtConfined']['fpcu']/section['wall']['CtConfined']['fpc'] > 0.90):
    print(f"Warning!!! fpccu/fpcc={section['wall']['CtConfined']['fpcu']/section['wall']['CtConfined']['fpc']:.2f} > 0.90")

print(f"epsccU\t= {section['wall']['CtConfined']['epscU']:.5f}")
if (section['wall']['CtConfined']['epscU']/section['wall']['CtConfined']['epsc0'] < 4.0):
    print(f"Warning!!! epsccU/epscc0={section['wall']['CtConfined']['epscU']/section['wall']['CtConfined']['epsc0']:.2f} < 4.0")
if (section['wall']['CtConfined']['epscU']/section['wall']['CtConfined']['epsc0'] > 8.7):
    print(f"Warning!!! epsccU/epscc0={section['wall']['CtConfined']['epscU']/section['wall']['CtConfined']['epsc0']:.2f} > 8.7")

if (section['wall']['r'] < 0.08):
    print(f"Warning!!! r={section['wall']['r']:.2f} < 0.08")
if (section['wall']['r'] > 0.7):
    print(f"Warning!!! r={section['wall']['r']:.2f} > 0.7")

if (section['wall']['Cd'] < 0.2):
    print(f"Warning!!! Cd={section['wall']['Cd']:.2f} < 0.2")
if (section['wall']['Cd'] > 0.75):
    print(f"Warning!!! Cd={section['wall']['Cd']:.2f} > 0.75")



#=============================================================================
#    Section Effective Stiffness:
#=============================================================================
# Flexural Stiffness
section['wall']['EIs_1'] = section['wall']['StWeb']['Es'] * section['wall']['I_Webs']
section['wall']['EIs_2'] = section['wall']['StFlange']['Es'] * section['wall']['I_Flanges']
section['wall']['EIs']   = section['wall']['EIs_1'] + section['wall']['EIs_2']
                         
section['wall']['EIc_1'] = section['wall']['CtUnconfined']['Ec']  * section['wall']['I_UnconfConc']
section['wall']['EIc_2'] = section['wall']['CtConfined']['Ec'] * section['wall']['I_ConfConc']
section['wall']['EIc']   = section['wall']['EIc_1'] + section['wall']['EIc_2']
                         
section['wall']['EIeff'] = 0.64 * (section['wall']['EIs'] + 0.6*section['wall']['EIc'])       # AISC 360-22, Eq. (I2-12) 
                         
# Axial Stiffness        
section['wall']['EAs_1'] = section['wall']['StWeb']['Es'] * section['wall']['A_Composite_St1']
section['wall']['EAs_2'] = section['wall']['StFlange']['Es'] * section['wall']['A_Composite_St2']
section['wall']['EAs']   = section['wall']['EAs_1'] + section['wall']['EAs_2']
                         
section['wall']['EAc_1'] = section['wall']['CtUnconfined']['Ec']  * section['wall']['A_Composite_Ct1']
section['wall']['EAc_2'] = section['wall']['CtConfined']['Ec'] * section['wall']['A_Composite_Ct2']
section['wall']['EAc']   = section['wall']['EAc_1'] + section['wall']['EAc_2']
                         
section['wall']['EAeff'] = 0.8 * (section['wall']['EAs'] + 0.45*section['wall']['EAc'])       # AISC 360-22, I1.5 


















