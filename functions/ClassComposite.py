exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
# exec(open("../Input/unitsSI.py").read()) # It SHOULD read and execute exec(open("Input/units    .py").read())
import sys
import numpy as np

class steel:
    def __init__(self, Es, Fy, Fu, eps_sh, eps_ult, nu, 
                 alpha, beta, gamma, Cf, a1, limit, R1, R2, R3):
        self.Es     = Es
        self.Esh    = self.Es/30
        self.Fy     = Fy 
        self.Fu     = Fu 
        self.epsy   = self.Fy/self.Es
        self.eps_sh = eps_sh
        self.eps_ult= eps_ult
        self.nu     = nu
        self.alpha  = alpha
        self.beta   = beta
        self.gamma  = gamma
        self.Cf     = Cf
        self.a1     = a1
        self.limit  = limit
        self.R1     = R1
        self.R2     = R2
        self.R3     = R3

class concrete:
    def __init__(self, fpc,  wc, lam):
        self.fpc        = fpc
        self.fpcu       = 1
        self.wc         = wc
        self.lam        = lam
        self.Ec         = (21.5e3*MPa * 1.0 * (abs(self.fpc/MPa)/10)**(1/3))            # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
        self.epsc0      = 2*self.fpc/self.Ec                                            # Crack width (Average of 0.15 to  0.25 mm)
        self.Gf         = (73 * (self.fpc/MPa)**0.18)                                   # Fracture Energy CEB-FIB-2010 section 5.1.5.2
        self.fts        = 1.0*(0.3 * (self.fpc/MPa - 8)**(2/3))*MPa                     # CEB-FIB-2010 Eq. (5.1-5)
        self.Ets        = abs(1/(1-(2*self.Ec*self.Gf)/(self.wc*self.fts**2)))*self.Ec
        

class compo:
    def __init__(self, tagSec, tagInt, ALR,
                 tw, Hw, Esw, Fyw, Fuw, eps_shw, eps_ultw, nuw, alphaw, betaw, gammaw, Cfw, a1w, limitw, R1w, R2w, R3w, 
                 Bf, tf, Esf, Fyf, Fuf, eps_shf, eps_ultf, nuf, alphaf, betaf, gammaf, Cff, a1f, limitf, R1f, R2f, R3f,
                 tc, fpc, wc, lamConf, lamUnconf,
                 lsr, b):
        
        self.tagSec     = tagSec
        self.tagInt     = tagInt
        self.ALR        = ALR
        self.lsr        = lsr
        self.b          = b
        self.St_flange  = steel(Esw, Fyw, Fuw, eps_shw, eps_ultw, nuw, alphaw, betaw, gammaw, Cfw, a1w, limitw, R1w, R2w, R3w)
        self.St_web     = steel(Esf, Fyf, Fuf, eps_shf, eps_ultf, nuf, alphaf, betaf, gammaf, Cff, a1f, limitf, R1f, R2f, R3f)
        self.Ct_unconf  = concrete(fpc,  wc, lamUnconf)
        self.Es         = (self.St_flange.Es        + self.St_web.Es        )/2
        self.Fy         = (self.St_flange.Fy        + self.St_web.Fy        )/2
        self.Fu         = (self.St_flange.Fu        + self.St_web.Fu        )/2
        self.eps_sh     = (self.St_flange.eps_sh    + self.St_web.eps_sh    )/2
        self.eps_ult    = (self.St_flange.eps_ult   + self.St_web.eps_ult   )/2
        self.nu         = (self.St_flange.nu        + self.St_web.nu        )/2
        self.alpha      = (self.St_flange.alpha     + self.St_web.alpha     )/2
        self.beta       = (self.St_flange.beta      + self.St_web.beta      )/2
        self.gamma      = (self.St_flange.gamma     + self.St_web.gamma     )/2
        self.Cf         = (self.St_flange.Cf        + self.St_web.Cf        )/2
        self.a1         = (self.St_flange.a1        + self.St_web.a1        )/2
        self.limit      = (self.St_flange.limit     + self.St_web.limit     )/2
        self.R1         = (self.St_flange.R1        + self.St_web.R1        )/2
        self.R2         = (self.St_flange.R2        + self.St_web.R2        )/2
        self.R3         = (self.St_flange.R3        + self.St_web.R3        )/2
        
        self.rhos           = (2*tw)/(tc + 2*tw) # Percentage of Steel
        self.R              = b/tw * (12*(1-self.nu**2)/(4*np.pi**2))**0.5 * (self.Fy/self.Es)**0.5 # Masoumeh Asgarpoor
        self.frp            = (-6.5*self.R*((self.Ct_unconf.fpc/MPa)**1.46/(self.Fy/MPa)) + 0.12*(self.Ct_unconf.fpc/MPa)**1.03)*MPa # Masoumeh Asgarpoor
        fpcc                = ((self.Ct_unconf.fpc/MPa) + 4*(self.frp/MPa)*(1+0.8*ALR)**3.5)*MPa # Masoumeh Asgarpoor
        self.Ct_conf        = concrete(fpcc, wc, lamConf)
        self.Ct_conf.Ec     = (21.5e3*MPa * 1.0 * (abs(self.Ct_conf.fpc/MPa)/10)**(1/3)) # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
        self.Ct_conf.epsc0  = 2*self.Ct_conf.fpc/self.Ct_conf.Ec
        self.Ct_conf.fpcu   = (0.15 *(self.Ct_unconf.fpc/MPa)** 1.5 * (self.Fy/MPa)**0.01 * self.rhos**0.16 * (1-ALR)**(-0.5) * lsr**(-0.025))*MPa # Masoumeh Asgarpoor 
        self.Ct_conf.epscU  = 0.157   *self.Ct_unconf.epsc0 **(-0.67) * (self.Ct_unconf.fpcu/MPa) **0.23 *(self.Fy/MPa)**(-1.4) * self.rhos**0.06 * (1-ALR)**(-0.17) * lsr**0.12 #Masoumeh Asgarpoor
        self.Ct_conf.fpcu   = (2.63 *(self.Ct_conf.fpc/MPa)**0.65 * (self.Fy/MPa)**0.001 * self.rhos**(-0.04) * (1-ALR)**( 0.4) * lsr**( 0.070))*MPa # Masoumeh Asgarpoor 
        self.Ct_conf.epscU  = 1.12e-6 *self.Ct_conf.epsc0**(-0.33) * (self.Ct_conf.fpcu/MPa)**0.83 *(self.Fy/MPa)**(0.77) * self.rhos**0.07 * (1-ALR)**( 0.15) * lsr**0.16 #Masoumeh Asgarpoor 
        self.r              = (15*lsr**0.37 * (self.Fy/self.Ct_unconf.fpc)**0.26 * self.eps_sh**0.3 * self.eps_ult**0.85)**-1 # Masoumeh Asgarpoor 
        self.Cd             = 16 * (self.Fy/self.Fu)**0.78 * self.eps_ult * ((self.Ct_unconf.fpcu/MPa)**0.5/(self.Ct_unconf.fpc/MPa))**0.58 * self.r**0.37 # Masoumeh Asgarpoor 
        
        
        
        
        self.d          = Hw + 2*tf
        self.Hc2        = (tc + 2*tw)/2     # Height of   confined concrete i.e. Region 2 in documentation # Masoumeh Asgharpoor
        self.Hc1        = Hw - 2*self.Hc2        # Height of unconfined concrete i.e. Region 1 in documentation
        if self.Hc1 < 0:
            print(f"Hw is {Hw}, but it cannot be less than {tc + 2*tw}"); sys.exit()
        self.St_web.A   = 2*(tw*Hw)
        self.St_flange.A= 2*(tf*Bf)
        self.Ct_unconf.A= self.Hc1 * tc
        self.Ct_conf.A  = self.Hc2 * tc * 2
        self.St_A       = self.St_flange.A + self.St_web.A
        self.Ct_A       = self.Ct_unconf.A + self.Ct_conf.A

        self.EIeff_webs     = self.St_web.Es    * (1/12 * (2*tw) * Hw**3)
        self.EIeff_flanges  = self.St_flange.Es * (1/12 * Bf * (self.d**3 - Hw**3))
        self.EIeff_St       = self.EIeff_webs + self.EIeff_flanges
        
        self.EIeff_unconf   = self.Ct_unconf.Ec * (1/12 * tc * self.Hc1**3)
        self.EIeff_conf     = self.Ct_conf.  Ec * (1/12 * tc * Hw**3 - 1/12 * tc * self.Hc1**3)
        self.EIeff_Ct       = self.EIeff_unconf + self.EIeff_conf
        
        self.EIeff          = self.EIeff_St + self.EIeff_Ct
        
        self.EAeff_webs     = self.St_web.Es    * self.St_web.A
        self.EAeff_flanges  = self.St_flange.Es * self.St_flange.A
        self.EAeff_St       = self.EAeff_webs   + self.EAeff_flanges
        
        self.EAeff_unconf   = self.Ct_unconf.Ec * self.Ct_unconf.A
        self.EAeff_conf     = self.Ct_conf.Ec   * self.Ct_conf.A
        self.EAeff_Ct       = self.EAeff_unconf + self.EAeff_conf
        
        self.EAeff          = self.EAeff_St + self.EAeff_Ct

# #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit, R1,    R2,   R3 ] 
# propWeb     = [3/16*inch, 0.24 *m,   200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01,  0.333, 18.0, 4.0]
# propFlange  = [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01,  0.333, 18.0, 4.0]
# #profCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
# profCore    = [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]
# lsr         = 48.
# b           = 114*mm
# beam = compo(1, 1, 0.1,*propWeb, *propFlange, *profCore, lsr, b)

# print(f"Es of flange material is {beam.St_flange.Es}")
# print(f"Es of web    material is {beam.St_web.Es}")
# print(f"Average Es the beam   is {beam.Es}")
# print(f"Depth of the beam is {beam.d}")
# print(f"EIeff = {beam.EIeff}")
# print(f"EAeff = {beam.EAeff}")








