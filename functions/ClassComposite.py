exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
# exec(open("../Input/unitsSI.py").read()) # It SHOULD read and execute exec(open("Input/units    .py").read())
import sys
import numpy                       as np
import openseespy.opensees         as ops
import matplotlib.pyplot           as plt
import opsvis                      as opv

class steel:
    def __init__(self, Es, Fy, Fu, eps_sh, eps_ult, nu, 
                 alpha, beta, gamma, Cf, a1, limit):
        self.Es     = Es
        self.Esh    = Es/30
        self.Fy     = Fy 
        self.Fu     = Fu 
        self.epsy   = Fy/Es
        self.eps_sh = eps_sh
        self.eps_ult= eps_ult
        self.nu     = nu
        self.alpha  = alpha
        self.beta   = beta
        self.gamma  = gamma
        self.Cf     = Cf
        self.a1     = a1
        self.limit  = limit
        self.A      = 1

class concrete:
    def __init__(self, fpc,  wc, lam):
        self.fpc        = fpc
        self.fpcu       = 1
        self.wc         = wc
        self.lam        = lam
        self.Ec         = (21.5e3*MPa * 1.0 * (abs(fpc/MPa)/10)**(1/3))            # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
        self.epsc0      = 2*fpc/self.Ec                                            # Crack width (Average of 0.15 to  0.25 mm)
        self.epscU      = 1
        self.Gf         = (73 * (fpc/MPa)**0.18)                                   # Fracture Energy CEB-FIB-2010 section 5.1.5.2
        self.fts        = 1.0*(0.3 * (fpc/MPa - 8)**(2/3))*MPa                     # CEB-FIB-2010 Eq. (5.1-5)
        self.Ets        = abs(1/(1-(2*self.Ec*self.Gf)/(wc*self.fts**2)))*self.Ec
        self.A          = 1
        

class compo:
    def __init__(self, tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf, P, lsr, b, NfibeY,
                 tw, Hw, Esw, Fyw, Fuw, eps_shw, eps_ultw, nuw, alphaw, betaw, gammaw, Cfw, a1w, limitw, 
                 Bf, tf, Esf, Fyf, Fuf, eps_shf, eps_ultf, nuf, alphaf, betaf, gammaf, Cff, a1f, limitf,
                 tc, fpc, wc, lamConf, lamUnconf
                 ):
        
        self.tagSec             = tagSec
        self.tagMatStFlange     = tagMatStFlange 
        self.tagMatStWeb        = tagMatStWeb    
        self.tagMatCtUnconf     = tagMatCtUnconf 
        self.tagMatCtConf       = tagMatCtConf   
        
        self.St_flange  = steel(Esw, Fyw, Fuw, eps_shw, eps_ultw, nuw, alphaw, betaw, gammaw, Cfw, a1w, limitw)
        self.St_web     = steel(Esf, Fyf, Fuf, eps_shf, eps_ultf, nuf, alphaf, betaf, gammaf, Cff, a1f, limitf)
        self.Ct_unconf  = concrete(fpc,  wc, lamUnconf)
        self.Ct_conf    = concrete(fpc,  wc, lamConf) # This is only to create Ct_conf
        
        self.d          = Hw + 2*tf
        self.Hc2        = Hc2 = (tc + 2*tw)/2           # Height of   confined concrete i.e. Region 2 in documentation # Masoumeh Asgharpoor
        self.Hc1        = Hc1 = Hw - 2*Hc2   # Height of unconfined concrete i.e. Region 1 in documentation
        if Hc1 < 0:
            print(f"Hw is {Hw}, but it cannot be less than {tc + 2*tw}"); sys.exit()
        self.St_web.A   = 2*(tw*Hw)
        self.St_flange.A= 2*(tf*Bf)
        self.Ct_unconf.A= self.Hc1 * tc
        self.Ct_conf.A  = self.Hc2 * tc * 2
        self.St_A       = self.St_flange.A + self.St_web.A
        self.Ct_A       = self.Ct_unconf.A + self.Ct_conf.A
        self.P          = P
        self.Pno        = 0.85*(self.Ct_A*abs(fpc)) + (self.St_web.A*abs(Fyw) + self.St_flange.A*abs(Fyf))
        ALR             = P/self.Pno
        self.lsr        = lsr
        self.b          = b
        self.NfibeY     = NfibeY
        self.tw         = tw
        self.Hw         = Hw
        self.Bf         = Bf
        self.tf         = tf
        self.tc         = tc
        self.Es         = Es        = (self.St_flange.Es        + self.St_web.Es        )/2
        self.Esh        = Esh       = (self.St_flange.Esh       + self.St_web.Esh       )/2
        self.Fy         = Fy        = (self.St_flange.Fy        + self.St_web.Fy        )/2
        self.Fu         = Fu        = (self.St_flange.Fu        + self.St_web.Fu        )/2
        self.eps_sh     = eps_sh    = (self.St_flange.eps_sh    + self.St_web.eps_sh    )/2
        self.eps_ult    = eps_ult   = (self.St_flange.eps_ult   + self.St_web.eps_ult   )/2
        self.nu         = nu        = (self.St_flange.nu        + self.St_web.nu        )/2
        self.alpha      = alpha     = (self.St_flange.alpha     + self.St_web.alpha     )/2
        self.beta       = beta      = (self.St_flange.beta      + self.St_web.beta      )/2
        self.gamma      = gamma     = (self.St_flange.gamma     + self.St_web.gamma     )/2
        self.Cf         = Cf        = (self.St_flange.Cf        + self.St_web.Cf        )/2
        self.a1         = a1        = (self.St_flange.a1        + self.St_web.a1        )/2
        self.limit      = limit     = (self.St_flange.limit     + self.St_web.limit     )/2
        
        epsc0, fpcu         =           self.Ct_unconf.epsc0, self.Ct_unconf.fpcu
        rhos                =           (2*tw)/(tc + 2*tw) # Percentage of Steel
        R                   =           b/tw * (12*(1-nu**2)/(4*np.pi**2))**0.5 * (Fy/Es)**0.5 # Masoumeh Asgarpoor
        frp                 =           (-6.5*R*((fpc/MPa)**1.46/(Fy/MPa)) + 0.12*(fpc/MPa)**1.03)*MPa # Masoumeh Asgarpoor
        fpcc                =           ((fpc/MPa) + 4*(frp/MPa)*(1+0.8*ALR)**3.5)*MPa # Masoumeh Asgarpoor
        self.Ct_conf        =           concrete(fpcc, wc, lamConf)
        self.Ct_conf.Ec     = Ecc =     (21.5e3*MPa * 1.0 * (abs(fpcc/MPa)/10)**(1/3)) # Tangent Modulus of Elasticity with fpc in MPa  ==> CEB-FIB-2010 5.1.7.2 (Selected by Masoumeh Asgharpoor)
        self.Ct_conf.epsc0  = epscc0 =  2*fpcc/Ecc
        self.Ct_unconf.fpcu = fpcu =    (0.15 *(fpc/MPa)** 1.5 * (Fy/MPa)**0.01 * rhos**0.16 * (1-ALR)**(-0.5) * lsr**(-0.025))*MPa # Masoumeh Asgarpoor 
        self.Ct_unconf.epscU= epscU =   0.157   *epsc0 **(-0.67) * (fpcu/MPa) **0.23 *(Fy/MPa)**(-1.4) * rhos**0.06 * (1-ALR)**(-0.17) * lsr**0.12 #Masoumeh Asgarpoor
        self.Ct_conf.fpcu   = fpccu =   (2.63 *(fpcc/MPa)**0.65 * (Fy/MPa)**0.001 * rhos**(-0.04) * (1-ALR)**(0.4) * lsr**(0.070))*MPa # Masoumeh Asgarpoor 
        self.Ct_conf.epscU  = epsccU =  1.12e-6 *epscc0**(-0.33) * (fpccu/MPa)**0.83 *(Fy/MPa)**(0.77) * rhos**0.07 * (1-ALR)**( 0.15) * lsr**0.16 #Masoumeh Asgarpoor 
        self.r              = r =       (15*lsr**0.37 * (Fy/fpc)**0.26 * eps_sh**0.3 * eps_ult**0.85)**-1 # Masoumeh Asgarpoor 
        self.Cd             = Cd =      16 * (Fy/Fu)**0.78 * eps_ult * ((fpcu/MPa)**0.5/(fpc/MPa))**0.58 * r**0.37 # Masoumeh Asgarpoor 
        
        
        
        

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
        
        # Define Materials
        self.tagMatStFlange = tagMatStFlange
        ops.uniaxialMaterial('ReinforcingSteel', tagMatStFlange, Fyf, Fuf, Esf, Esh, eps_shf, eps_ultf, 
                             '-GABuck', lsr, beta, r, gamma, 
                             '-CMFatigue', Cf, alpha, Cd, 
                             '-IsoHard', a1, limit
                             )
        self.tagMatStWeb    = tagMatStWeb
        ops.uniaxialMaterial('ReinforcingSteel', tagMatStWeb, Fyw, Fuw, Esw, Esh, eps_shw, eps_ultw, 
                             '-GABuck', lsr, beta, r, gamma, 
                             '-CMFatigue', Cf, alpha, Cd, 
                             '-IsoHard', a1, limit
                             )
        ops.uniaxialMaterial('Concrete02', tagMatCtUnconf, fpc,  epsc0,  fpcu,  self.Ct_unconf.epscU, lamUnconf, self.Ct_unconf.fts, self.Ct_unconf.Ets)
        ops.uniaxialMaterial('Concrete02', tagMatCtConf,   fpcc, epscc0, fpccu, self.Ct_conf.epscU,   lamConf,   self.Ct_conf.fts,   self.Ct_conf.Ets)
        
        
        # Define Fiber Section For Testing
        if 1:
            GJ = 1e6
            # Section Geometry
            ##  Bottom Flange
            crdsI1 = [-(Hw/2 + tf), -Bf/2       ]
            crdsJ1 = [- Hw/2      ,  Bf/2       ]
            ##  Top Flange
            crdsI4 = [  Hw/2      , -Bf/2       ]
            crdsJ4 = [ (Hw/2 + tf),  Bf/2       ]
            ##  Left Web
            crdsI2 = [-Hw/2       , -(tc/2 + tw)]
            crdsJ2 = [ Hw/2       , - tc/2      ]
            ##  Right Web
            crdsI3 = [-Hw/2       ,   tc/2      ]
            crdsJ3 = [ Hw/2       ,  (tc/2 + tw)]
            ##  Concrete Core - Unconfined
            crdsI6 = [-Hc1/2      , -tc/2       ]
            crdsJ6 = [ Hc1/2      ,  tc/2       ]
            ##  Concrete Core - Confined
            crdsI5 = [-Hw/2       , -tc/2       ]
            crdsJ5 = [-Hc1/2      ,  tc/2       ]
            crdsI7 = [ Hc1/2      , -tc/2       ]
            crdsJ7 = [ Hw/2       ,  tc/2       ]
            
            divider= 10
            times  = max(1, int((Hw/tf)             /(divider)))
            times1 = max(1, int((Hc1/tf)            /(divider)))
            times2 = max(1, int((((Hw-Hc1)/2)/tf)   /(divider)))
            

            # this part of the code is just to sent out a varibale for plotting the fiber section
            fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],
    
                     ['patch', 'rect', tagMatStFlange,  NfibeY,        1, *crdsI1, *crdsJ1], #Bot Flange
                     ['patch', 'rect', tagMatStFlange,  NfibeY,        1, *crdsI4, *crdsJ4], #Top Flange
                     ['patch', 'rect', tagMatStWeb,     NfibeY*times,  1, *crdsI2, *crdsJ2], #Left Web
                     ['patch', 'rect', tagMatStWeb,     NfibeY*times,  1, *crdsI3, *crdsJ3], #Right Web
                     ['patch', 'rect', tagMatCtConf,    NfibeY*times2, 1, *crdsI5, *crdsJ5], #Concrete Core bot
                     ['patch', 'rect', tagMatCtUnconf,  NfibeY*times1, 1, *crdsI6, *crdsJ6], #Concrete Core mid
                     ['patch', 'rect', tagMatCtConf,    NfibeY*times2, 1, *crdsI7, *crdsJ7], #Concrete Core top
                     ]
        
            matcolor = ['y', 'b', 'r', 'g', 'y', 'b', 'r', 'g', 'm', 'k', 'y', 'b', 'r', 'g', 'm', 'k']
            opv.plot_fiber_section(fib_sec, matcolor=matcolor)
            plt.axis('equal')
            
            plt.show()
        
        
# #tags       = [tagSec, tagMatStFlange, tagMatStWeb, tagMatCtUnconf, tagMatCtConf]
# tags        = [1,      1,              2,           3,              4           ]
# #propStPart = [B,         H,         Es,      Fy,      Fu,      eps_sh, eps_ult, nu,   alpha, beta, gamma, Cf,  a1,  limit] 
# propWeb     = [3/16*inch, 1    *m,   200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# propFlange  = [11*inch,   3/16*inch, 200*GPa, 422*MPa, 473*MPa, 0.007,  0.12,    0.28, 0.65,  1.0,  1.0,   0.5, 4.3, 0.01]
# #propCore   = [tc,     fpc,    wc,     lamConf, lamUnconf]
# propCore    = [9*inch, 50*MPa, 0.2*mm, 0.05,    0.25     ]
# lsr         = 48.
# b           = 114*mm
# NfibeY      = 5
# #beam= compo(*tags, ALR, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
# beam = compo(*tags, 0.1, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)

# print(f"Es of flange material is {beam.St_flange.Es}")
# print(f"Es of web    material is {beam.St_web.Es}")
# print(f"Average Es the beam   is {beam.Es}")
# print(f"Depth of the beam is {beam.d}")
# print(f"EIeff = {beam.EIeff}")
# print(f"EAeff = {beam.EAeff}")









