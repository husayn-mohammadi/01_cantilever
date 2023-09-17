exec(open("MAIN.py").readlines()[20]) # It SHOULD read and execute exec(open("Input/materialParameters.py").read())

import sys
import openseespy.opensees as ops

#=============================================================================
#    Functions:
#=============================================================================

def matSteel(typeMat, tagMatSt):
    if tagMatSt == 1:
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatSt, Es1)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatSt, Es1, 0.002)
        elif typeMat == 'Steel02':
            ops.uniaxialMaterial('Steel02', tagMatSt, Fy1, Es1, 0.002)
        elif typeMat == 'ReinforcingSteel':
            #   uniaxialMaterial('ReinforcingSteel', tagMatSt, Fy, Fu, Es, Esh, eps_sh, eps_ult, '-GABuck', lsr, beta, r, gamma, '-DMBuck', lsr, alpha, '-CMFatigue', Cf, alpha, Cd, '-IsoHard', a1=4.3, limit=1.0, '-MPCurveParams', R1=0.333, R2=18.0, R3=4.0)
            ops.uniaxialMaterial(*['ReinforcingSteel', tagMatSt, Fy1, Fu1, Es1, Esh1, eps_sh1, eps_ult1, 
                                   '-GABuck', lsr, beta, r, gamma, 
                                   '-CMFatigue', Cf, alpha1, Cd, 
                                   '-IsoHard', a1, limit
                                   ])
        else:
            print('UNKNOWN steel material!!!');sys.exit()
            
    elif tagMatSt == 2:
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatSt, Es2)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatSt, Es2, 0.002)
        elif typeMat == 'Steel02':
            ops.uniaxialMaterial('Steel02', tagMatSt, Fy2, Es2, 0.002)
        elif typeMat == 'ReinforcingSteel':
            #   uniaxialMaterial('ReinforcingSteel', tagMatSt, Fy, Fu, Es, Esh, eps_sh, eps_ult, '-GABuck', lsr, beta, r, gamma, '-DMBuck', lsr, alpha, '-CMFatigue', Cf, alpha, Cd, '-IsoHard', a1=4.3, limit=1.0, '-MPCurveParams', R1=0.333, R2=18.0, R3=4.0)
            ops.uniaxialMaterial(*['ReinforcingSteel', tagMatSt, Fy2, Fu2, Es2, Esh2, eps_sh2, eps_ult2, 
                                   '-GABuck', lsr, beta, r, gamma, 
                                   '-CMFatigue', Cf, alpha2, Cd, 
                                   '-IsoHard', a1, limit
                                   ])
        else:
            print('UNKNOWN steel material!!!');sys.exit()
    else: 
        print('UNAVAILABLE tagMatSt!!!');sys.exit()
        

def matConcrete(typeMat, tagMatCt):
    if tagMatCt == 3: # For unconfined concrete
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatCt, Ec)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatCt, Ec, 0.002)
        elif typeMat == 'Concrete01':
            ops.uniaxialMaterial('Concrete01', tagMatCt, fpc, epsc0, fpcu, epscU)
        elif typeMat == 'Concrete02':
            ops.uniaxialMaterial('Concrete02', tagMatCt, fpc, epsc0, fpcu, epscU, lam, fts, Ets)
        else:
            print('UNKNOWN concrete material!!!');sys.exit()
    elif tagMatCt == 4: # For confined concrete
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatCt, Ecc)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatCt, Ecc, 0.002)
        elif typeMat == 'Concrete01':
            ops.uniaxialMaterial('Concrete01', tagMatCt, fpcc, epscc0, fpccu, epsccU)
        elif typeMat == 'Concrete02':
            ops.uniaxialMaterial('Concrete02', tagMatCt, fpcc, epscc0, fpccu, epsccU, lam, fts, Ets)
        else:
            print('UNKNOWN concrete material!!!');sys.exit()
    else: 
        print('UNAVAILABLE tagMatCt!!!');sys.exit()







































