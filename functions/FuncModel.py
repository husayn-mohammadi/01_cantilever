exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())

import sys
import openseespy.opensees as ops



def buildCantileverN(tagSec, L, PlasticHingeLength=1, numSeg=3, typeEle='dispBeamColumn', modelFoundation=True):#
    
    maxIter     = 10
    tol         = 1e-12
    
    #       Define Geometric Transformation
    tagGTLinear = 1
    tagGTPDelta = 2
    ops.geomTransf('Linear', tagGTLinear)
    ops.geomTransf('PDelta', tagGTPDelta)
    
    
    #       Define beamIntegrator
    tagInt      = 1
    NIP         = 5
    ops.beamIntegration('Legendre', tagInt, tagSec, NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
             
    #       Define Nodes & Elements
    ##      Define Base Node
    tagBaseNode = 1
    ops.node(tagBaseNode, 0., 0.)
    ops.fix( tagBaseNode, 1, 1, 1)
    
    ##      Define Foundation Node
    tagFndnNode = 2
    ops.node(tagFndnNode, 0., 0.)
    
    if modelFoundation == True:
        ops.fix( tagFndnNode, 1,  1, 0)
    else:
        ops.fix( tagFndnNode, 1,  1, 1)
        
    k_rot       = 8400000 *kip*inch
    ops.uniaxialMaterial('Elastic',   100000, k_rot)
    # ops.uniaxialMaterial('ElasticPP', 100000, k_rot, 0.002)
    
    #   element('zeroLength', eleTag, *eleNodes,                    '-mat', *matTags, '-dir', *dirs)
    ops.element('zeroLength', 100000, *[tagBaseNode, tagFndnNode],  '-mat', 100000,   '-dir', 3)
    
    #       Define Elements
    ##      Define Nonlinear Elements
    for i in range(0, numSeg):
        
        ops.node(i+1+tagFndnNode, 0., ((i+1)/numSeg)*PlasticHingeLength)
        
        if typeEle == 'forceBeamColumn':
            #   element('forceBeamColumn', eleTag,   *eleNodes,                         transfTag,   integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)
            ops.element('forceBeamColumn', i+1,      *[i+tagFndnNode, i+1+tagFndnNode], tagGTPDelta, tagInt,         '-iter', maxIter,    tol)
        elif typeEle == 'dispBeamColumn':
            #   element('dispBeamColumn',  eleTag,   *eleNodes,                         transfTag,   integrationTag, '-cMass', '-mass', mass=0.0)
            ops.element('dispBeamColumn',  i+1,      *[i+tagFndnNode, i+1+tagFndnNode], tagGTPDelta, tagInt)
        else:
            print('UNKNOWN element type!!!');sys.exit()
            

    ##      Define Linear Element
    tagTopNode  = numSeg + tagFndnNode + 1
    ops.node(tagTopNode, 0., L)
    
    #   element('elasticBeamColumn', eleTag,   *eleNodes,                                       secTag, transfTag, <'-mass', mass>, <'-cMass'>, <'-release', releaseCode>)
    ops.element('elasticBeamColumn', numSeg+1, *[numSeg+tagFndnNode, numSeg + tagFndnNode + 1], tagSec, tagGTPDelta)
    
    return(tagTopNode, tagFndnNode)

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


def buildShearCritBeam(tagSec, L, numSeg=3, typeEle='dispBeamColumn'):
    
    maxIter     = 10
    tol         = 1e-12
    
    #       Define Geometric Transformation
    tagGTLinear = 1
    ops.geomTransf('Linear', tagGTLinear)
    
    
    #       Define beamIntegrator
    tagInt      = 1
    NIP         = 5
    ops.beamIntegration('Legendre', tagInt, tagSec, NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
    
    #       Define Nodes & Elements
    ##      Define Base Node
    tagBaseNode = 1
    ops.node(tagBaseNode, 0., 0.)
    ops.fix( tagBaseNode, 1, 1, 1)
    
    #       Define Elements
    ##      Define Nonlinear Elements
    for i in range(0, numSeg):
        
        ops.node(i+1+tagBaseNode, 0., ((i+1)/numSeg)*L)
        
        if typeEle == 'forceBeamColumn':
            #   element('forceBeamColumn', eleTag,   *eleNodes,                         transfTag,   integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)
            ops.element('forceBeamColumn', i+1,      *[i+tagBaseNode, i+1+tagBaseNode], tagGTLinear, tagInt,         '-iter', maxIter,    tol)
        elif typeEle == 'dispBeamColumn':
            #   element('dispBeamColumn',  eleTag,   *eleNodes,                         transfTag,   integrationTag, '-cMass', '-mass', mass=0.0)
            ops.element('dispBeamColumn',  i+1,      *[i+tagBaseNode, i+1+tagBaseNode], tagGTLinear, tagInt)
        else:
            print('UNKNOWN element type!!!');sys.exit()
                 
    tagTopNode = numSeg+1
    ops.fix(tagTopNode, 0, 1, 1)
    return(tagTopNode, tagBaseNode)


# ops.wipe()
# ops.model('basic', '-ndm', 2, '-ndf', 3)
# makeSectionRect(1, 1, 1, 350, 200000)
# makeSectionI(2, 1, 1, 0.1, 0.2, 350, 200000)
# buildCantileverL(3, 200e9, 1, 1)
# ops.wipe()









