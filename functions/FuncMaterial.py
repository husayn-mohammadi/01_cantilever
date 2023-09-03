exec(open("MAIN.py").readlines()[19]) # It SHOULD read and execute exec(open("Input/inputData.py").read())

import sys
import openseespy.opensees as ops

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







































