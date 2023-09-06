exec(open("MAIN.py").readlines()[19]) # It SHOULD read and execute exec(open("Input/inputData.py").read())

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
                                   '-GABuck', lsr1, beta1, r1, gamma1, 
                                   '-CMFatigue', Cf1, alpha1, Cd1, 
                                   '-IsoHard', a1_1, limit1
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
                                   '-GABuck', lsr2, beta2, r2, gamma2, 
                                   '-CMFatigue', Cf2, alpha2, Cd2, 
                                   '-IsoHard', a1_2, limit2
                                   ])
        else:
            print('UNKNOWN steel material!!!');sys.exit()
    else: 
        print('UNAVAILABLE tagMatSt!!!');sys.exit()
        

def matConcrete(typeMat, tagMatCt):
    if tagMatCt == 3:
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatCt, Ec1)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatCt, Ec1, 0.002)
        elif typeMat == 'Concrete02':
            ops.uniaxialMaterial('Concrete02', tagMatCt, fpc1, epsc01, fpcu1, epsU1, lam1, ft1, Ets1)
        else:
            print('UNKNOWN concrete material!!!');sys.exit()
    elif tagMatCt == 4:
        if typeMat == 'Elastic':
            ops.uniaxialMaterial('Elastic', tagMatCt, Ec2)
        elif typeMat == 'ElasticPP':
            ops.uniaxialMaterial('ElasticPP', tagMatCt, Ec2, 0.002)
        elif typeMat == 'Concrete02':
            ops.uniaxialMaterial('Concrete02', tagMatCt, fpc2, epsc02, fpcu2, epsU2, lam2, ft2, Ets2)
        else:
            print('UNKNOWN concrete material!!!');sys.exit()
    else: 
        print('UNAVAILABLE tagMatCt!!!');sys.exit()







































