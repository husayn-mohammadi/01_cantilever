exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())

import sys
import openseespy.opensees as ops



def buildCantileverN(L, tagSec, typeEle='forceBeamColumn', PlasticHingeLength=1):
    
    maxIter     = 10
    tol         = 1e-12
             
    # Define Nodes 
    ops.node(1, 0., 0.)
    ops.node(2, 0., PlasticHingeLength)
    ops.node(3, 0., L)
        
    # Assign boundary constraints
    ops.fix(1, 1, 1, 1)
    
    # Define Geometric Transformation
    tagGTLinear = 1
    tagGTPDelta = 2
    ops.geomTransf('Linear', tagGTLinear)
    ops.geomTransf('PDelta', tagGTPDelta)
    
    
    # Define beamIntegrator
    tagInt      = 1
    Nintegr     = 4
    ops.beamIntegration('Lobatto', tagInt, tagSec, Nintegr)
    
    # Define Elements
    
    ## Nonlinear Element:
    if typeEle == 'forceBeamColumn':
        #   element('forceBeamColumn', eleTag, *eleNodes, transfTag,   integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)
        ops.element('forceBeamColumn', 1,      *[1, 2],   tagGTPDelta, tagInt,         '-iter', maxIter,    tol)
    elif typeEle == 'dispBeamColumn':
        #   element('dispBeamColumn',  eleTag, *eleNodes, transfTag,   integrationTag, '-cMass', '-mass', mass=0.0)
        ops.element('dispBeamColumn',  1,      *[1, 2],   tagGTPDelta, tagInt)
    else:
        print('UNKNOWN element type!!!');sys.exit()
    
    ## Linear Element
    #   element('elasticBeamColumn', eleTag, *eleNodes, secTag, transfTag, <'-mass', mass>, <'-cMass'>, <'-release', releaseCode>)
    ops.element('elasticBeamColumn', 2,      *[2, 3],   tagSec, tagGTPDelta)

def buildCantileverL(L, E, I, A):
    
    # Define Nodes
    ops.node(1, 0., 0.)
    ops.node(2, 0., L )
        
    # Assign boundary constraints
    ops.fix(1, 1, 1, 1)
    
    # Define Geometric Transformation
    tagGTLinear = 1
    tagGTPDelta = 2
    ops.geomTransf('Linear', tagGTLinear)
    ops.geomTransf('PDelta', tagGTPDelta)
    
    # Define Element
    ops.element('elasticBeamColumn', 1, *[1, 2], A, E, I, tagGTPDelta)





# ops.wipe()
# ops.model('basic', '-ndm', 2, '-ndf', 3)
# makeSectionRect(1, 1, 1, 350, 200000)
# makeSectionI(2, 1, 1, 0.1, 0.2, 350, 200000)
# buildCantileverL(3, 200e9, 1, 1)
# ops.wipe()









