import numpy as np

exec(open("MAIN.py").readlines()[18])               # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())
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

fpc         = 50.9 *MPa                                             # Masoumeh Asgharpoor: scope of study 32.5<fpc<102 (MPa)
print(f"fpc\t\t= {fpc/MPa:.2f} MPa")
# Ec        = 4700*abs(fpc/MPa)**0.5s                               # With fpc in MPa  ==> ACI 318 - 2019 SI
# Ec        = 57000*abs(fpc)**0.5                                   # With fpc in psi  ==> ACI 318 - 2019 US
# Ec        = (57000*abs(fpc*1000)**0.5)/1000                       # With fpc in ksi  ==> ACI 318 - 2019 US
Ec          = (21.5e3*MPa * 1.0 * (abs(fpc/MPa)/10)**(1/3))         # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
# Ec        = 4840 *ksi
print(f"Ec\t\t= {Ec/MPa:.2f} MPa")
epsc0       = 2*fpc/Ec
print(f"epsc0\t= {epsc0:.5f}")
lam1        = 0.25                                                   # Unconfined Concrete
lam2        = 0.05                                                   # Confined Concrete
fts         = 1.0*(0.3 * (fpc/MPa - 8)**(2/3))*MPa                   # CEB-FIB-2010 Eq. (5.1-5)
print(f"fts\t\t= {fts/MPa:.2f} MPa")
wc          = 0.2 *mm                                               # Crack width (Average of 0.15 to  0.25 mm)
Gf          = (73 * (fpc/MPa)**0.18)/1000   #(unitsSI_kN.py)        # Fracture Energy CEB-FIB-2010 section 5.1.5.2 (Since the force unit is kN it is divided by 1000)
Ets         = abs(1/(1-(2*Ec*Gf)/(wc*fts**2)))*Ec                   # Article: THE INFLUENCE OF AGGREGATE SIZE ON THE WIDTH OF FRACTURE PROCESS ZONE IN CONCRETE MEMBERS

print(f"Ets\t\t= {Ets/MPa:.2f} MPa")

#=============================================================================
#    Steel Parameters:
#=============================================================================
nu          = 0.28

## Steel Material No. 1 (For Webs of the Composite Walls)
Es1         = 200   *GPa
Fy1         = 422   *MPa
Esh1        = Es1/30
Fu1         = 473   *MPa
epsy1       = Fy1/Es1
eps_sh1     = 0.007
eps_ult1    = 0.12
alpha1      = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)

## Steel Material No. 2 (For Flanges of the Composite Walls)
Es2         = Es1     
Fy2         = Fy1     
Esh2        = Esh1    
Fu2         = Fu1     
epsy2       = epsy1   
eps_sh2     = eps_sh1 
eps_ult2    = eps_ult1
alpha2      = 0.65 # Fatigue Ductility Exponent (For ASTM A572 alpha=0.65 and for ASTM A36 alpha=0.55)

section['wall']['b']           = 114 *mm  # minimum unsupported width of confined region in composite wall cross-section
section['wall']['lsr']         = 48. # lsr = lu/db = 12**0.5 * lu/tw
beta        = 1.0
gamma       = 1.0
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
print(f"Fy\t\t= {Fy/MPa:.2f} MPa")
Es          = (Es1 + Es2)/2
print(f"Es\t\t= {Es/MPa:.2f} MPa")
Fu          = (Fu1 + Fu2)/2
print(f"Fu\t\t= {Fu/MPa:.2f} MPa")
eps_sh      = (eps_sh1  + eps_sh2)/2
print(f"eps_sh\t= {eps_sh:.5f}")
eps_ult     = (eps_ult1 + eps_ult2)/2
print(f"eps_ult\t= {eps_ult:.5f}")

section['wall']['rhos']        = (2*section['wall']['tw'])/(section['wall']['tw']) # Percentage of Steel

section['wall']['R']           = section['wall']['b']/section['wall']['tw'] * (12*(1-nu**2)/(4*np.pi**2))**0.5 * (Fy/Es)**0.5                    # Masoumeh Asgarpoor

# frp = 3.76*MPa
section['wall']['frp']         = (-6.5*section['wall']['R']*((fpc/MPa)**1.46/(Fy/MPa)) + 0.12*(fpc/MPa)**1.03)*MPa            # Masoumeh Asgarpoor

# fpcc = 62.88*MPa
section['wall']['fpcc']        = ((fpc/MPa) + 4*(section['wall']['frp']/MPa)*(1+0.8*ALR)**3.5)*MPa                            # Masoumeh Asgarpoor
print(f"fpcc\t= {section['wall']['fpcc']/MPa:.2f} MPa")
section['wall']['Ecc']         = (21.5e3*MPa * 1.0 * (abs(section['wall']['fpcc']/MPa)/10)**(1/3))                            # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
print(f"Ecc\t\t= {section['wall']['Ecc']/MPa:.2f} MPa")

# epscc0 = 0.0034
section['wall']['epscc0']      = 2*section['wall']['fpcc']/section['wall']['Ecc']
print(f"epscc0\t= {section['wall']['epscc0']:.5f}")

# fpcu = 27.56*MPa
section['wall']['fpcu']        = (0.15 *(fpc/MPa)** 1.5  * (Fy/MPa)**0.01  * section['wall']['rhos']**0.16    * (1-ALR)**(-0.5) * section['wall']['lsr']**(-0.025))*MPa                    # Masoumeh Asgarpoor 
print(f"fpcu\t= {section['wall']['fpcu']/MPa:.2f} MPa")
if (section['wall']['fpcu']/fpc < 0.45):
    print(f"Warning!!! fpcu/fpc={section['wall']['fpcu']/fpc:.2f} < 0.45")
if (section['wall']['fpcu']/fpc > 0.80):
    print(f"Warning!!! fpcu/fpc={section['wall']['fpcu']/fpc:.2f} > 0.80")

# epscU = 0.0049 
section['wall']['epscU']       = 0.157   *epsc0 **(-0.67) * (section['wall']['fpcu']/MPa) **0.23 *(Fy/MPa)**(-1.4) * section['wall']['rhos']**0.06 * (1-ALR)**(-0.17) * section['wall']['lsr']**0.12    #Masoumeh Asgarpoor
print(f"epscU\t= {section['wall']['epscU']:.5f}")
if (section['wall']['epscU']/epsc0 < 1.6):
    print(f"Warning!!! epscU/epsc0={section['wall']['epscU']/epsc0:.2f} < 1.6")
if (section['wall']['epscU']/epsc0 > 5.5):
    print(f"Warning!!! epscU/epsc0={section['wall']['epscU']/epsc0:.2f} > 5.5")

# fpccu = 56.95*MPa
section['wall']['fpccu']       = (2.63 *(section['wall']['fpcc']/MPa)**0.65 * (Fy/MPa)**0.001 * section['wall']['rhos']**(-0.04) * (1-ALR)**( 0.4) * section['wall']['lsr']**( 0.070))*MPa                    # Masoumeh Asgarpoor 
print(f"fpccu\t= {section['wall']['fpccu']/MPa:.2f} MPa")
if (section['wall']['fpccu']/section['wall']['fpcc'] < 0.45):
    print(f"Warning!!! fpccu/fpcc={section['wall']['fpccu']/section['wall']['fpcc']:.2f} < 0.45")
if (section['wall']['fpccu']/section['wall']['fpcc'] > 0.90):
    print(f"Warning!!! fpccu/fpcc={section['wall']['fpccu']/section['wall']['fpcc']:.2f} > 0.90")

# epsccU = 0.0291
section['wall']['epsccU']      = 1.12e-6 *section['wall']['epscc0']**(-0.33) * (section['wall']['fpccu']/MPa)**0.83 *(Fy/MPa)**(0.77) * section['wall']['rhos']**0.07 * (1-ALR)**( 0.15) * section['wall']['lsr']**0.16    #Masoumeh Asgarpoor 
print(f"epsccU\t= {section['wall']['epsccU']:.5f}")
if (section['wall']['epsccU']/section['wall']['epscc0'] < 4.0):
    print(f"Warning!!! epsccU/epscc0={section['wall']['epsccU']/section['wall']['epscc0']:.2f} < 4.0")
if (section['wall']['epsccU']/section['wall']['epscc0'] > 8.7):
    print(f"Warning!!! epsccU/epscc0={section['wall']['epsccU']/section['wall']['epscc0']:.2f} > 8.7")

# r = 0.327
section['wall']['r']           = (15*section['wall']['lsr']**0.37 * (Fy/fpc)**0.26 * eps_sh**0.3 * eps_ult**0.85)**-1                                 # Masoumeh Asgarpoor 
if (section['wall']['r'] < 0.08):
    print(f"Warning!!! r={section['wall']['r']:.2f} < 0.08")
if (section['wall']['r'] > 0.7):
    print(f"Warning!!! r={section['wall']['r']:.2f} > 0.7")

# Cd = 0.42
section['wall']['Cd']          = 16 * (Fy/Fu)**0.78 * eps_ult * ((section['wall']['fpcu']/MPa)**0.5/(fpc/MPa))**0.58 * section['wall']['r']**0.37                                    # Masoumeh Asgarpoor 
if (section['wall']['Cd'] < 0.2):
    print(f"Warning!!! Cd={section['wall']['Cd']:.2f} < 0.2")
if (section['wall']['Cd'] > 0.75):
    print(f"Warning!!! Cd={section['wall']['Cd']:.2f} > 0.75")



#=============================================================================
#    Section Effective Stiffness:
#=============================================================================
# Flexural Stiffness
section['wall']['EIs_1'] = Es1 * section['wall']['I_Webs']
section['wall']['EIs_2'] = Es2 * section['wall']['I_Flanges']
section['wall']['EIs']   = section['wall']['EIs_1'] + section['wall']['EIs_2']
                         
section['wall']['EIc_1'] = Ec  * section['wall']['I_UnconfConc']
section['wall']['EIc_2'] = section['wall']['Ecc'] * section['wall']['I_ConfConc']
section['wall']['EIc']   = section['wall']['EIc_1'] + section['wall']['EIc_2']
                         
section['wall']['EIeff'] = 0.64 * (section['wall']['EIs'] + 0.6*section['wall']['EIc'])       # AISC 360-22, Eq. (I2-12) 
                         
# Axial Stiffness        
section['wall']['EAs_1'] = Es1 * section['wall']['A_Composite_St1']
section['wall']['EAs_2'] = Es2 * section['wall']['A_Composite_St2']
section['wall']['EAs']   = section['wall']['EAs_1'] + section['wall']['EAs_2']
                         
section['wall']['EAc_1'] = Ec  * section['wall']['A_Composite_Ct1']
section['wall']['EAc_2'] = section['wall']['Ecc'] * section['wall']['A_Composite_Ct2']
section['wall']['EAc']   = section['wall']['EAc_1'] + section['wall']['EAc_2']
                         
section['wall']['EAeff'] = 0.8 * (section['wall']['EAs'] + 0.45*section['wall']['EAc'])       # AISC 360-22, I1.5 


















