# exec(open("functions/units.py").read())
exec(open("functions/unitsUS.py").read())

import sys
import openseespy.opensees as ops

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
#    Functions:
#=============================================================================

def matSteel(typeMat, tagMatSt):
    if typeMat == 'Elastic':
        ops.uniaxialMaterial('Elastic', tagMatSt, Es)
    elif typeMat == 'ElasticPP':
        ops.uniaxialMaterial('ElasticPP', tagMatSt, Es, 0.002)
    elif typeMat == 'Steel02':
        ops.uniaxialMaterial('Steel02', tagMatSt, Fy, Es, b)
    elif typeMat == 'ReinforcingSteel':
        #   uniaxialMaterial('ReinforcingSteel', tagMatSt, Fy, Fu, Es, Esh, eps_sh, eps_ult, '-GABuck', lsr, beta, r, gamma, '-DMBuck', lsr, alpha, '-CMFatigue', Cf, alpha, Cd, '-IsoHard', a1=4.3, limit=1.0, '-MPCurveParams', R1=0.333, R2=18.0, R3=4.0)
        ops.uniaxialMaterial(*['ReinforcingSteel', tagMatSt, Fy, Fu, Es, Esh, eps_sh, eps_ult, 
                               '-GABuck', lsr, beta, r, gamma, 
                               '-CMFatigue', Cf, alpha, Cd, 
                               '-IsoHard', a1, limit
                               ])
        
    else:
        print('UNKNOWN steel material!!!');sys.exit()

def matConcrete(typeMat, tagMatCt):
    if typeMat == 'Elastic':
        ops.uniaxialMaterial('Elastic', tagMatCt, Ec)
    elif typeMat == 'ElasticPP':
        ops.uniaxialMaterial('ElasticPP', tagMatCt, Ec, 0.002)
    elif typeMat == 'Concrete02':
        ops.uniaxialMaterial('Concrete02', tagMatCt, fpc, epsc0, fpcu, epsU, lam, ft, Ets)
    else:
        print('UNKNOWN concrete material!!!');sys.exit()







































