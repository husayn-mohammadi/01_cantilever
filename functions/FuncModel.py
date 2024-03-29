exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
exec(open("MAIN.py").readlines()[19]) # It SHOULD read and execute exec(open("Input/inputData.py").read())
import sys
import openseespy.opensees     as ops
# import functions.FuncSection   as fs
# import functions.FuncPlot      as fp
from functions.ClassComposite import compo

def buildCantileverN(L, P, PlasticHingeLength=1, numSeg=3, modelFoundation=True, linearity=False, typeEle='dispBeamColumn'):#
    
    #       Define Geometric Transformation
    tagGTLinear = 1
    tagGTPDelta = 2
    ops.geomTransf('Linear', tagGTLinear)
    ops.geomTransf('PDelta', tagGTPDelta)

    NIP         = 9
    #       Define beamIntegrator
    nameSect    = 'wall'
    tags        = Section[nameSect]['tags']
    propWeb     = Section[nameSect]['propWeb']
    propFlange  = Section[nameSect]['propFlange']
    propCore    = Section[nameSect]['propCore']
    #wall       = compo("wall", *tags, P, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
    composite   = compo("wall", *tags, P, lsr, b, NfibeY, *propWeb, *propFlange, *propCore, linearity)
    compo.printVar(composite)
    EIeff       = composite.EIeff
    EAeff       = composite.EAeff
    EE          = EIeff
    AA          = EAeff/EIeff
    compo.defineSection(composite)

    ops.beamIntegration('Legendre', tags[0], tags[0], NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
             
    #       Define Nodes & Elements
    ##      Define Base Node
    tagNodeBase = 1
    ops.node(tagNodeBase, 0., 0.)
    ops.fix( tagNodeBase, 1, 1, 1)
    
    ##      Define Foundation Node
    tagNodeFndn = 2
    ops.node(tagNodeFndn, 0., 0.)
    
    if modelFoundation == True:
        ops.equalDOF(tagNodeBase, tagNodeFndn, 1, 2)
        k_rot       = 20*EIeff/L; print(f"k_rot = {k_rot}"); ops.uniaxialMaterial('Elastic',   100000, k_rot)
        #   element('zeroLength', eleTag, *eleNodes,                    '-mat', *matTags, '-dir', *dirs)
        ops.element('zeroLength', 100000, *[tagNodeBase, tagNodeFndn],  '-mat', 100000,   '-dir', 3)
    else:
        ops.equalDOF(tagNodeBase, tagNodeFndn, 1, 2, 3)
    
    #       Define Elements
    ##      Define Nonlinear Elements
    for i in range(0, numSeg):
        
        ops.node(i+1+tagNodeFndn, 0., ((i+1)/numSeg)*PlasticHingeLength)
        
        if typeEle == 'forceBeamColumn':
            #   element('forceBeamColumn', eleTag,   *eleNodes,                         transfTag,   integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)
            ops.element('forceBeamColumn', i+1,      *[i+tagNodeFndn, i+1+tagNodeFndn], tagGTPDelta, tags[0],         '-iter', 100,    1e-6)
        elif typeEle == 'dispBeamColumn':
              # element('dispBeamColumn',  eleTag,   *eleNodes,                         transfTag,   integrationTag, '-cMass', '-mass', mass=0.0)
            ops.element('dispBeamColumn',  i+1,      *[i+tagNodeFndn, i+1+tagNodeFndn], tagGTPDelta, tags[0])
            # ops.element('elasticBeamColumn',i+1,     *[i+tagNodeFndn, i+1+tagNodeFndn], tags[0],tagGTPDelta)
            # ops.element('elasticBeamColumn', i+1,     *[i+tagNodeFndn, i+1+tagNodeFndn], AA, EE, 1, tagGTLinear)
        else:
            print('UNKNOWN element type!!!');sys.exit()
            

    ##      Define Linear Element
    tagNodeTop  = numSeg + tagNodeFndn + 1
    ops.node(tagNodeTop, 0., L)
    
    # ops.element('dispBeamColumn',  numSeg+1, *[numSeg+tagNodeFndn, numSeg + tagNodeFndn + 1], tagGTPDelta, tags[0])
    #   element('elasticBeamColumn', eleTag,   *eleNodes,                                       secTag, transfTag, <'-mass', mass>, <'-cMass'>, <'-release', releaseCode>)
    # ops.element('elasticBeamColumn', numSeg+1, *[numSeg+tagNodeFndn, numSeg + tagNodeFndn + 1], tags[0], tagGTPDelta)
    ops.element('elasticBeamColumn', numSeg+1, *[numSeg+tagNodeFndn, numSeg + tagNodeFndn + 1], AA, EE, 1, tagGTLinear)
    
    mass = P/g
    ops.mass(tagNodeTop, *[mass,mass,1e-8])
    
    tagElementWallBase = [1]
    return(tagNodeTop, tagNodeBase, tagElementWallBase, composite)

def subStructBeam(tagEleGlobal, tagNodeI, tagNodeJ, tagGT, section, PlasticHingeLength, numSeg=3, rotSpring = False):
    tagEleLocal = 100*tagEleGlobal
    coordsLocal = {
        tagNodeI: ops.nodeCoord(tagNodeI),
        tagNodeJ: ops.nodeCoord(tagNodeJ),
        }
    tagCoordXI  = f"{tagNodeI}"[3:-1]
    tagCoordYI  = f"{tagNodeI}"[1:-3]
    tagCoordXJ  = f"{tagNodeJ}"[3:-1]
    tagCoordYJ  = f"{tagNodeJ}"[1:-3]
    
    Lx = abs(coordsLocal[tagNodeJ][0] - coordsLocal[tagNodeI][0])
    Ly = abs(coordsLocal[tagNodeJ][1] - coordsLocal[tagNodeI][1])
    L  = (Lx**2 + Ly**2)**0.5
    if PlasticHingeLength/L >= 0.5:
        print("PlasticHingeLength >= L/2"); sys.exit()
    
    delta = PlasticHingeLength/numSeg
    tagNodeII = tagEleLocal-1
    tagNodeJJ = tagEleLocal+1
    
    for i in range(numSeg+1):
        coordsLocal[tagNodeII-i] = [coordsLocal[tagNodeI][0]+i*delta/L*Lx, coordsLocal[tagNodeI][1]+i*delta/L*Ly]
        ops.node(tagNodeII-i, *coordsLocal[tagNodeII-i])
        coordsLocal[tagNodeJJ+i] = [coordsLocal[tagNodeJ][0]-i*delta/L*Lx, coordsLocal[tagNodeJ][1]-i*delta/L*Ly]
        ops.node(tagNodeJJ+i, *coordsLocal[tagNodeJJ+i])
        if i > 0:
            ops.element('dispBeamColumn',   tagNodeII-i, *[tagNodeII-i, tagNodeII-i+1], tagGT, section.tagSec) # for now instead of tagGTLinear I have written 1
            ops.element('dispBeamColumn',   tagNodeJJ+i, *[tagNodeJJ+i, tagNodeJJ+i-1], tagGT, section.tagSec) # for now instead of tagGTLinear I have written 1
    
    ops.element('elasticBeamColumn',tagEleGlobal, *[tagNodeII-numSeg, tagNodeJJ+numSeg], section.AA, section.EE, 1, tagGT) # I=1 (+) for now instead of tagGTLinear I have written 1
    
    # Here is the place for adding the rotational springs
    eAve = section.eAve; print(f"eAve = {eAve}")
    if rotSpring == True:
        if L <= eAve:
            ops.equalDOF(tagNodeI, tagNodeII, 1)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags,          '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXI}{tagCoordXJ}{tagCoordYI}"), *[tagNodeI, tagNodeII], '-mat', *[100002, 100001], '-dir', *[2, 3])
            ops.equalDOF(tagNodeJJ, tagNodeJ, 1)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags,          '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXJ}{tagCoordXI}{tagCoordYJ}"), *[tagNodeJJ, tagNodeJ], '-mat', *[100002, 100001], '-dir', *[2, 3])
        else:
            ops.equalDOF(tagNodeI, tagNodeII, 1, 2)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags, '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXI}{tagCoordXJ}{tagCoordYI}"), *[tagNodeI, tagNodeII], '-mat', 100001,   '-dir', 3)
            ops.equalDOF(tagNodeJJ, tagNodeJ, 1, 2)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags, '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXJ}{tagCoordXI}{tagCoordYJ}"), *[tagNodeJJ, tagNodeJ], '-mat', 100001,   '-dir', 3)
    else:
        if L <= eAve:
            ops.equalDOF(tagNodeI, tagNodeII, 1, 3)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags,          '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXI}{tagCoordXJ}{tagCoordYI}"), *[tagNodeI, tagNodeII], '-mat', *[100002], '-dir', *[2])
            ops.equalDOF(tagNodeJJ, tagNodeJ, 1, 3)
            #   element('zeroLength', eleTag,                                         *eleNodes,              '-mat', *matTags,          '-dir', *dirs)
            ops.element('zeroLength', int(f"89{tagCoordXJ}{tagCoordXI}{tagCoordYJ}"), *[tagNodeJJ, tagNodeJ], '-mat', *[100002], '-dir', *[2])
        else:
            ops.equalDOF(tagNodeI,  tagNodeII, 1, 2, 3)
            ops.equalDOF(tagNodeJJ, tagNodeJ,  1, 2, 3)
    
    tagEleFibRec = tagNodeII-1
    
    return tagEleFibRec

def buildBeam(L, PlasticHingeLength=1, numSeg=3, rotSpring=True):
        
    #       Define Geometric Transformation
    tagGTLinear = 1
    ops.geomTransf('Linear', tagGTLinear)
    
    NIP         = 5
    #       Define beamIntegrator
    nameSect    = 'beam'
    tags        = Section[nameSect]['tags']
    propWeb     = Section[nameSect]['propWeb']
    propFlange  = Section[nameSect]['propFlange']
    propCore    = Section[nameSect]['propCore']
    #composite  = compo("beam", *tags, P, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
    composite   = compo("beam", *tags, 0, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
    compo.printVar(composite)
    EIeff       = composite.EIeff; k_rot = 20*EIeff/L; print(f"k_rot2 = {k_rot}"); ops.uniaxialMaterial('Elastic',   100001, k_rot)
    EAeff       = composite.EAeff
    composite.EE= EIeff
    composite.AA= EAeff/EIeff
    compo.defineSection(composite)
    ops.beamIntegration('Legendre', tags[0], tags[0], NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
             
    #       Define Nodes & Elements
    ##      Define Base Node
    tagNodeBase = 1
    ops.node(tagNodeBase, 0., 0.)
    ops.fix( tagNodeBase, 1, 1, 1)
    
    ##      Define Top Node
    tagNodeTop  = 2
    ops.node(tagNodeTop, 0., L)
    ops.fix( tagNodeTop, 0, 1, 1)
        
    tagEleGlobal = 1
    
    tagEleFibRec = subStructBeam(tagEleGlobal, tagNodeBase, tagNodeTop, tagGTLinear, composite, PlasticHingeLength, numSeg, rotSpring)
    # print(f"tagEleFibRec = {tagEleFibRec}")
    return(tagNodeTop, tagNodeBase, [tagEleFibRec], composite)

def buildShearCritBeam(L, numSeg=3, typeEle='dispBeamColumn'):
    L       = (520 *mm) * 1
    #       Define Geometric Transformation
    tagGTLinear = 1
    ops.geomTransf('Linear', tagGTLinear)
    
    #       Define beamIntegrator
    NIP         = 5
    nameSect    = 'beam'
    tags        = Section[nameSect]['tags']
    propWeb     = Section[nameSect]['propWeb']
    propFlange  = Section[nameSect]['propFlange']
    propCore    = Section[nameSect]['propCore']
    #wall       = compo("beam", *tags, P, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
    composite   = compo("beam", *tags, P, lsr, b, NfibeY, *propWeb, *propFlange, *propCore)
    compo.printVar(composite)
    fs.makeSectionBoxComposite(composite)
    ops.beamIntegration('Legendre', tags[0], tags[0], NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
    
    #       Define Nodes & Elements
    ##      Define Base Node
    tagNodeBase = 1
    ops.node(tagNodeBase, 0., 0.)
    
    ##      Define 1st Mid Node
    tagNodeMid1 = 2
    ops.node(tagNodeMid1, 0., 0.)
    
    ##      Define 2nd Mid Node
    tagNodeMid2 = 3
    ops.node(tagNodeMid2, 0., L)
    
    ##      Define Top Node
    tagNodeTop = 4
    ops.node(tagNodeTop, 0., L)
    
    # Boundary Costraints
    ops.fix(tagNodeBase, 1, 1, 1)
    ops.fix(tagNodeTop, 0, 1, 1)
    ops.equalDOF(tagNodeBase, tagNodeMid1, 2)
    ops.equalDOF(tagNodeTop, tagNodeMid2, 2)
    
    
    

    #       MATERIAL DEFINITIONS
    E0                  = 200 *GPa                          # Kelastic (ksi)
    G                   = E0/(2*(1+0.3))                    # Shear modulus (ksi)
    Fy                  = 228 * MPa
    
    ##      Link Flexural-Hinge Material (Q11)
    h                   = 350 *mm
    b                   = 170 *mm
    tw                  = 10 *mm
    tf                  = 12 *mm
    # A                   = h*b - (h-2*tf)*(b-tw)
    Ashear              = h*tw;                                         print(f"Av = {Ashear*1000**2:.0f} mm2")
    I                   = 1/12 * (b*h**3 - (b-tw)*(h-2*tf)**3);         print(f"I = {I*1000**4:.0f} mm4")
    S                   = I/(h/2);                                      print(f"S = {S*1000**3:.0f} mm3")
    Z                   = (b*tf) * (h-tf) + (h-2*tf)*tw/2 * (h-2*tf)/2; print(f"Z = {Z*1000**3:.0f} mm3")
    ShapeFactor         = Z/S;                                          print(f"ShapeFactor = {ShapeFactor:.3f}")
    Mp                  = Z*Fy;                                         print(f"Mp = {Mp:.1f} kN.m")
    k_rot               = 6*E0*I/L                          # 6 for both ends fixed
    tagMatHinge         = 10                                # HingeMat Identifier
    ops.uniaxialMaterial('Steel01', tagMatHinge, Mp, k_rot, 0.001)

    ##      Link Spring Shear Material
    shearMaterialModel  = "Steel02"
    tagMatSpring        = 20                                # SpringMat Identifier
    Vp                  = 0.6*Fy*Ashear;                                print(f"Vp = {Vp:.1f} kN")
    print(f"emax = {2*Mp/Vp*1000:.0f} mm")
    # print(f"2.6Mp/L = {2.6*Mp/L:.1f} kN")
    print(f"2.0Mp/L = {2.0*Mp/L:.1f} kN")
    # print(f"1.6Mp/L = {1.6*Mp/L:.1f} kN")
    k_trans             = 2*G*Ashear/L  
    if shearMaterialModel == "Steel02":
        b1              = 0.003                             # Ratio of Kyield to Kelastic
        R0,cR1,cR2      = 18.5, 0.9, 0.1                    # cR1 specifies the radius. 10<=R0<=20
        a1= a3          = 0.06
        a2 = a4         = 1.0
        ops.uniaxialMaterial('Steel02', tagMatSpring, Vp, k_trans, b1, *[R0,cR1,cR2], *[a1, a2, a3, a4])
    elif shearMaterialModel == "Steel4":
        b_k             = 0.0035
        R0, r1, r2      = 8.0, 0.9, 0.25
        b_i             = 0.0005
        b_l             = 0.005
        rho_i, R_i, l_yp= 2, 8.0, 0.0
        f_u, R_u        = Vp, 8
        #   uniaxialMaterial('Steel4', matTag,       Fy, E0,      '-kin', b_k, R0, r1, r2, '-iso', b_i, rho_i, b_l, R_i, l_yp, '-ult', f_u, R_u)
        ops.uniaxialMaterial('Steel4', tagMatSpring, Vp, k_trans, '-kin', b_k, R0, r1, r2, '-iso', b_i, rho_i, b_l, R_i, l_yp, '-ult', f_u, R_u)
    else:
        print("Unknown Material Model!!!\nThe program stopped at FuncModel/buildShearCritBeam!"); sys.exit()
    
    ##      Define Nonlinear Elements (Option2: 2 dispBeamColumn + 1 zeroLength(amongst))
    # ops.element('forceBeamColumn',   1, *[tagNodeMid1, tagNodeMid2], tagGTLinear, tagInt, '-iter', 10, 1e-12)
    ops.element('elasticBeamColumn', 1, *[tagNodeMid1, tagNodeMid2], tags[0], tagGTLinear)
    
    #   element('zeroLength', eleTag, *eleNodes,                    '-mat', *matTags,                       '-dir', *dirs, <'-doRayleigh', rFlag=0>, <'-orient', *vecx, *vecyp>)
    ops.element('zeroLength', 2,      *[tagNodeBase, tagNodeMid1],  '-mat', *[tagMatHinge, tagMatSpring],   '-dir', *[3, 1])
    ops.element('zeroLength', 3,      *[tagNodeMid2, tagNodeTop],   '-mat', *[tagMatHinge, tagMatSpring],   '-dir', *[3, 1])
    
    return(tagNodeTop, tagNodeBase)

#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%
#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%
#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%
#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%
#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%
#$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%

def coupledWalls(H_story_List, L_Bay_List, Lw, P, load, numSegBeam, numSegWall, PHL_wall, PHL_beam, SBL, typeCB="discretizedAllFiber", plot_section=True, modelFoundation=False, rotSpring=False, linearity=False):
    
    # k_rot       = 0.4*8400000 *kip*inch # Foundations Rotational Spring
    # ops.uniaxialMaterial('Elastic',   100000, k_rot)
    
    # k_rot       = 0.05*8400000 *kip*inch # Coupling Beams Rotational Spring
    # ops.uniaxialMaterial('Elastic',   100001, k_rot)
    
    modelLeaning = True     # True False
    
    for L_Bay in L_Bay_List:
        if L_Bay <= Lw:
            print(f"L_Bay={L_Bay} <= Lw={Lw}")
            print('The program will exit now!'); sys.exit()
    
    # gridList        = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    H_story_List    += [0]
    L_Bay_List      += [0]
    
    
    
    coords          = {}
    y               = 0.
    for storyNum, storyH in enumerate(H_story_List):
        # storyKey        = f"Story_{storyNum:02}"
        # print(storyKey)
        # print(f"Story Elevation = {y}")
        
        x           = 0.
        for gridIndex, L_Bay in enumerate(L_Bay_List):
            # gridKey         = f"{gridList[gridIndex]}"
            # print(gridKey)
            # print(f"Grid x = {x}")
            tagNode         = int(f"1{storyNum:02}{gridIndex:02}0") # This is to create tagNode for wall MAIN nodes
            coords[tagNode] = [x, y]
            
            if gridIndex == 0 and y != 0: # This is to create tagNode for nodes at right side of wall in 1st x-grid (in each story level except for base)
                tagNode     = int(f"1{storyNum:02}{gridIndex:02}2")
                coords[tagNode] = [x+Lw/2, y]
            elif gridIndex > 0 and gridIndex < len(L_Bay_List)-1 and y != 0: # This is to create tagNode for nodes at both side of wall in 1st x-grid (in each story level except for base)
                tagNode     = int(f"1{storyNum:02}{gridIndex:02}1")
                coords[tagNode] = [x-Lw/2, y]
                tagNode     = int(f"1{storyNum:02}{gridIndex:02}2")
                coords[tagNode] = [x+Lw/2, y]
                
            x               += L_Bay
        y               += storyH
            
    gridLeaningColumn = f"{(len(L_Bay_List)-1):02}"
    
    #   Build Model
    # ops.wipe()
    # ops.model('basic', '-ndm', 2, '-ndf', 3)
    
    #   Define Nodes
    for tagNode, coord in coords.items():
        # tagCoordY   = f"{tagNode}"[1:-3]
        # tagSuffix   = f"{tagNode}"[-1]
        ops.node(tagNode, *coord)
        # if tagCoordY == '00' and tagSuffix != '0': #this is to skip the nodes at base whose suffices are not 0
        #     continue
        # else:
        #     # print(f"tagNode = {tagNode}\tcoord = {coord}")
        #     ops.node(tagNode, *coord)
    
    #   Put base node tags into a list
    tagNodeBaseList = []
    for tagNode, coord in coords.items():
        tagCoordY   = f"{tagNode}"[1:-3]
        if tagCoordY == '00':
            tagNodeBaseList.append(tagNode)
    
    #   Assign Constraints
    # ops.fixY(0, *[1, 1, 1], '-tol', 1e-3)
    for node in tagNodeBaseList[:-1]:
        ops.fix(node, *[1, 1, 1])
    # print(tagNodeBaseList[-1])
    ops.fix(tagNodeBaseList[-1], *[1, 1, 0])
    
    #   Assign Nodal Masses: ops.mass(nodeTag, *massValues)
    
    ##  Define gravity loading nodes
    tagNodeLoad={}; tagNodeLoad["wall"]=[]; tagNodeLoad["leaningColumn"]=[]
    for tagNode, coord in coords.items():
        tagCoordXI  = f"{tagNode}"[3:-1]
        tagCoordYI  = f"{tagNode}"[1:-3]
        tagSuffixI  = f"{tagNode}"[-1]
        if tagSuffixI == '0' and tagCoordYI != '00' and tagCoordXI != gridLeaningColumn:
            tagNodeLoad["wall"].append(tagNode)
        elif tagSuffixI == '0' and tagCoordYI != '00' and tagCoordXI == gridLeaningColumn:
            tagNodeLoad["leaningColumn"].append(tagNode)

    ## Assigning Masses
    mass={}; mass["wall"] = load["wall"]/g; mass["leaningColumn"] = load["leaningColumn"]/g
    massValuesT = [mass["wall"], mass["wall"], 1e-8]
    massValuesL = [mass["leaningColumn"], mass["leaningColumn"], 1e-8]
    
    for element, tagNodes in tagNodeLoad.items():
        if element == "wall":               ###  Tributary Masses
            for tagNode in tagNodes:
                ops.mass(tagNode, *massValuesT)
        elif element == "leaningColumn":    ###  Leaning Column Masses
            for tagNode in tagNodes:
                ops.mass(tagNode, *massValuesL)
    
    ##  Assigning equalDOF for rigid diaphragm
    for element, tagNodes in tagNodeLoad.items():
        if element == "wall":               ###  Tributary Masses
            for tagNode in tagNodes:
                tagNodeI    = tagNode
                tagCoordXI  = int(f"{tagNodeI}"[3:-1])
                tagCoordYI  = int(f"{tagNodeI}"[1:-3])
                for tagNode in tagNodes:
                    tagNodeJ    = tagNode
                    tagCoordXJ  = int(f"{tagNodeJ}"[3:-1])
                    tagCoordYJ  = int(f"{tagNodeJ}"[1:-3])
                    if tagCoordYI == tagCoordYJ and tagCoordXJ - tagCoordXI == 1:
                        ops.equalDOF(tagNodeI, tagNodeJ, 1)
                        print(f"tagNodeI = {tagNodeI}\ttagNodeJ = {tagNodeJ}")
                
    
    #   for deciding whether to model the leaning columns
    if modelLeaning == False:
        print(f"Width of the Building is {x} meters.")
        ops.fixX(x, *[1, 1, 1], '-tol', 1e-3)
    
    #   Define Geometric Transformation
    tagGTLinear = 1
    tagGTPDelta = 2
    ops.geomTransf('Linear', tagGTLinear)
    ops.geomTransf('PDelta', tagGTPDelta)
    
    #   Define beamIntegrator
    NIP         = 7
    nameSect    = 'wall'
    tags        = Section[nameSect]['tags']
    propWeb     = Section[nameSect]['propWeb']
    propFlange  = Section[nameSect]['propFlange']
    propCore    = Section[nameSect]['propCore']
    #wall       = compo("wall", *tags, P, lsr, b,     NfibeY, *propWeb, *propFlange, *propCore)
    wall        = compo("wall", *tags, P, lsr, 0.114, NfibeY, *propWeb, *propFlange, *propCore, linearity)
    compo.printVar(wall)
    EIeff       = wall.EIeff; k_rot = 20*EIeff/y; print(f"k_rot1 = {k_rot}"); ops.uniaxialMaterial('Elastic',   100000, k_rot) # 4* is to consider 12EI/L instead of 3EI/L
    EAeff       = wall.EAeff; k_elo = 20*EAeff/y; print(f"k_elo = {k_elo}"); ops.uniaxialMaterial('Elastic',   100003, k_elo) # 4* is to consider 12EI/L instead of 3EI/L
    wall.EE     = EIeff
    wall.AA     = EAeff/EIeff
    compo.defineSection(wall) # This will create the fiber section
    ops.beamIntegration('Legendre', tags[0], tags[0], NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
    
    NIP         = 7
    nameSect    = 'beam'
    tags        = Section[nameSect]['tags']
    propWeb     = Section[nameSect]['propWeb']
    propFlange  = Section[nameSect]['propFlange']
    propCore    = Section[nameSect]['propCore']
    #beam       = compo("beam", *tags, P, lsr, b,     NfibeY, *propWeb, *propFlange, *propCore)
    beam        = compo("beam", *tags, 0, lsr, 0.114, NfibeY, *propWeb, *propFlange, *propCore, linearity)
    compo.printVar(beam)
    EIeff       = wall.EIeff; k_rot = 4*20*EIeff/L_CB; print(f"k_rot2 = {k_rot}"); ops.uniaxialMaterial('Elastic',   100001, k_rot)
    Av          = beam.St_web.A; G=beam.St_web.Es/(2*(1+0.3)); k_trans=20*2*G*Av/SBL/10; b1=0.003; R0,cR1,cR2= 18.5, 0.9, 0.1; a1=a3= 0.06; a2=a4= 1.0; Vp=0.6*beam.St_web.Fy*Av; 
    ops.uniaxialMaterial('Steel02', 100002, Vp, k_trans, b1, *[R0,cR1,cR2], *[a1, a2, a3, a4])
    EAeff       = wall.EAeff
    beam.EE     = EIeff
    beam.AA     = EAeff/EIeff
    compo.defineSection(beam) # This will create the fiber section
    ops.beamIntegration('Legendre', tags[0], tags[0], NIP)  # 'Lobatto', 'Legendre' for the latter NIP should be odd integer.
    
    #   Define material and sections
    A, E, I = 1e1, 200e9, 1e-2
    tagMatTruss     = 99
    ops.uniaxialMaterial('Elastic', tagMatTruss, E)
    
    #######################################################################################################
    # Define Element
    #######################################################################################################
    #   Walls:
    ##  Define tags of Walls and LeaningColumns
    
    def discretizeWall(tagNodeI, tagNodeJ, tagCoordXI, tagCoordYI, tagCoordYJ, Walls, coordsGlobal, PHL_wall, numSegWall=1, modelFoundation=False):
        
        xI  = coordsGlobal[tagNodeI][0];    yI  = coordsGlobal[tagNodeI][1]
        xJ  = coordsGlobal[tagNodeJ][0];    yJ  = coordsGlobal[tagNodeJ][1]
        
        Lx  = xJ - xI; Ly = yJ - yI
        L   = (Lx**2 + Ly**2)**0.5
        PHR = PHL_wall/L
        lx  = PHR*Lx/numSegWall; ly = PHR*Ly/numSegWall
        
        coordsLocal = {}
        tagNode = tagNodeI + 1
        coordsLocal[tagNode] = [xI + 0*lx, yI + 0*ly]
        ops.node(tagNode, *coordsLocal[tagNode])
        
        if modelFoundation == True:
            ops.equalDOF(tagNodeI, tagNode, 2)
            #   element('zeroLength', eleTag,                                            *eleNodes,             '-mat', *matTags, '-dir', *dirs)
            ops.element('zeroLength', int(f"88{tagCoordXI}"), *[tagNodeI, tagNode],  '-mat', *[100000, 100003],   '-dir', *[3, 1])
        else:
            ops.equalDOF(tagNodeI, tagNode, 1, 2, 3)
            
        for i in range(2, numSegWall+2):
            tagNode = tagNodeI + i
            coordsLocal[tagNode] = [xI + (i-1)*lx, yI + (i-1)*ly]
            ops.node(tagNode, *coordsLocal[tagNode])
            tagElement = int(f"5{tagCoordXI}{tagCoordYI}{tagCoordYJ}{i-1}")
            Walls[tagElement]  = [tagNode-1, tagNode ]
            # print(f"Wall{tagElement} = {Walls[tagElement]}")
            # print(f"NodeI({tagNode-1}) = {coordsLocal[tagNode-1]}")
            # print(f"NodeJ({tagNode}) = {coordsLocal[tagNode]}")
        tagElement = int(f"5{tagCoordXI}{tagCoordYI}{tagCoordYJ}{0}")
        Walls[tagElement] = [tagNode,   tagNodeJ]
        # print(f"Wall{tagElement} = {Walls[tagElement]}")
        # print(f"NodeI({tagNode}) = {coordsLocal[tagNode]}")
        # print(f"NodeJ({tagNodeJ}) = {coordsGlobal[tagNodeJ]}")
        # print("End")
        # return(0)
        
    Walls           = {}
    LeaningColumns  = {}
    for tagNode, coord in coords.items():
        # print("LOOP1:")
        # print(f"tagNode = {tagNode}\tcoord = {coord}")
        if f"{tagNode}"[-1] == '0': # To distinguish the main nodes
            tagNodeI    = tagNode
            tagCoordXI  = f"{tagNodeI}"[3:-1]
            tagCoordYI  = f"{tagNodeI}"[1:-3]
            # print(f"tagCoordXI = {tagCoordXI}\ttagCoordYI = {tagCoordYI}")
        for tagNode, coord in coords.items():
            # print("LOOP2:")
            # print(f"tagNode = {tagNode}\tcoord = {coord}")
            if f"{tagNode}"[-1] == '0': # To distinguish the main nodes
                tagNodeJ    = tagNode
                tagCoordXJ  = f"{tagNodeJ}"[3:-1]
                tagCoordYJ  = f"{tagNodeJ}"[1:-3]
                # print(f"tagCoordXJ = {tagCoordXJ}\ttagCoordYJ = {tagCoordYJ}")
                
                if tagCoordXI == tagCoordXJ: # this makes it a column
                    # print("tagCoordXI == tagCoordXJ")
                    if int(tagCoordYJ) - int(tagCoordYI) == 1: 
                        # print("int(tagCoordYJ) - int(tagCoordYI) == 1")
                        # print(f"tagCoordXI={tagCoordXI}    gridLeaningColumn={gridLeaningColumn}")
                        if tagCoordXI != gridLeaningColumn:
                            # print("tagCoordXI != gridLeaningColumn")
                            # print(f"{tagNodeI} VS {tagNodeJ} ==> tagWall = 5{tagCoordXI}{tagCoordYI}{tagCoordYJ}")
                            if int(tagCoordYJ) == 1:
                                # print("int(tagCoordYJ) == 1")
                                discretizeWall(tagNodeI, tagNodeJ, tagCoordXI, tagCoordYI, tagCoordYJ, Walls, coords, PHL_wall, numSegWall)
                                # Walls[f"5{tagCoordXI}{tagCoordYI}{tagCoordYJ}"] = [tagNodeI, tagNodeJ]  #Prefix 5 is for Walls
                            else:
                                # print("int(tagCoordYJ) != 1")
                                tagElement = int(f"5{tagCoordXI}{tagCoordYI}{tagCoordYJ}{0}")
                                Walls[tagElement] = [tagNodeI, tagNodeJ]  #Prefix 5 is for Walls
                        else:
                            tagElement = int(f"2{tagCoordXI}{tagCoordYI}{tagCoordYJ}")
                            LeaningColumns[tagElement] = [tagNodeI, tagNodeJ]  #Prefix 2 is for LeaningColumns
    
    ##  Define Walls
    for tagElement, tagNodes in Walls.items():
        # print(f"tagElement = {tagElement} & tanNodes = {tagNodes}")
        if f"{tagElement}"[-1] == '0':
            # print(f"tagElement = {tagElement} and tagNodes = {tagNodes}")
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, section['wall']['tagSec'], tagGTPDelta)
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, I, tagGTPDelta)
            ops.element('elasticBeamColumn', tagElement, *tagNodes, wall.AA, wall.EE, 1, tagGTPDelta) 
        else:
            ops.element('dispBeamColumn',    tagElement, *tagNodes, tagGTPDelta, wall.tagSec)
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, tagSec, tagGTPDelta)
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, I, tagGTPDelta)
    
    ## Define tag of Wall base elements as an output for stress-strain curve
    tagElementWallBase = []
    for tagElement, tagNodes in Walls.items():
        if f"{tagElement}"[-1] == '1':
            tagElementWallBase.append(tagElement)
    print("tagElementWallBase = {tagElementWallBase}")
    
    ##  Define LeaningColumns
    if modelLeaning == True:
        for tagElement, tagNodes in LeaningColumns.items():
            # print(f"tagElement = {tagElement} & tanNodes = {tagNodes}")
            # ops.element('Truss', tagElement, *tagNodes, A, tagMatTruss)
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, tagSec, tagGTPDelta)
            ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, 1e-10*I, tagGTPDelta)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #   Rigid Beams:
    ##  Define tags of Rigid Beams
    RBeams = {}
    for tagNode, coord in coords.items():
        tagNodeI    = tagNode
        tagCoordXI  = f"{tagNodeI}"[3:-1]
        tagCoordYI  = f"{tagNodeI}"[1:-3]
        tagSuffixI  = f"{tagNodeI}"[-1]
        for tagNode, coord in coords.items():
            tagNodeJ    = tagNode
            tagCoordXJ  = f"{tagNodeJ}"[3:-1]
            tagCoordYJ  = f"{tagNodeJ}"[1:-3]
            tagSuffixJ  = f"{tagNodeJ}"[-1]
            
            if tagCoordXI == tagCoordXJ and tagCoordYI == tagCoordYJ and (tagCoordYI != '00' or tagCoordYJ != '00'):
                if tagSuffixJ == '0' or tagSuffixI == '0':
                    if int(tagSuffixJ)-int(tagSuffixI) == -1 or int(tagSuffixJ)-int(tagSuffixI) == 2:
                        # print(f"{tagNodeI} VS {tagNodeJ} ==> tagRBeam = 5{tagCoordYI}{tagCoordXI}{tagSuffixI}{tagSuffixJ}")
                        tagElement = int(f"6{tagCoordYI}{tagCoordXI}{tagSuffixI}{tagSuffixJ}")
                        RBeams[tagElement] = [tagNodeI, tagNodeJ]  #Prefix 6 is for RBeams
                    
    ##  Define Rigid Beams
    for tagElement, tagNodes in RBeams.items():
        # print(f"tagElement = {tagElement} & tanNodes = {tagNodes}")
        ops.element('elasticBeamColumn', tagElement, *tagNodes, 1e0*A, 1e0*E, 1e10*I, tagGTLinear)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    def discretizeBeam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, Beams, coordsGlobal, numSegBeam=1):
        
        xI  = coordsGlobal[tagNodeI][0];    yI  = coordsGlobal[tagNodeI][1]
        xJ  = coordsGlobal[tagNodeJ][0];    yJ  = coordsGlobal[tagNodeJ][1]
        
        Lx = xJ - xI; Ly = yJ - yI
        
        lx = Lx/numSegBeam; ly = Ly/numSegBeam
        
        coordsLocal = {}
        for i in range(0, numSegBeam):
            tagNode = tagNodeI + i
            coordsLocal[tagNode] = [xI + i*lx, yI + i*ly]
            if i > 0:
                ops.node(tagNode, *coordsLocal[tagNode])
                tagElement = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}{i}")
                Beams[tagElement]  = [tagNode-1, tagNode ]
        tagElement = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}{numSegBeam}")
        Beams[tagElement] = [tagNode,   tagNodeJ]
        
        # return(0)
    
    # # Spring Material Properties
    # E0                  = 200 *GPa                          # Kelastic (ksi)
    # G                   = E0/(2*(1+0.3))                    # Shear modulus (ksi)
    # Fy                  = 228 * MPa
    
    # h                   = 350 *mm
    # b                   = 170 *mm
    # tw                  = 10 *mm
    # tf                  = 12 *mm
    
    # Ashear              = h*tw;                                         print(f"Av = {Ashear*1000**2:.0f} mm2")
    # I                   = 1/12 * (b*h**3 - (b-tw)*(h-2*tf)**3);         print(f"I = {I*1000**4:.0f} mm4")
    # S                   = I/(h/2);                                      print(f"S = {S*1000**3:.0f} mm3")
    # Z                   = (b*tf) * (h-tf) + (h-2*tf)*tw/2 * (h-2*tf)/2; print(f"Z = {Z*1000**3:.0f} mm3")
    # ShapeFactor         = Z/S;                                          print(f"ShapeFactor = {ShapeFactor:.3f}")
    # Mp                  = Z*Fy;                                         print(f"Mp = {Mp:.1f} kN.m")
    # k_rot               = 6*E0*I/SBL                        # 6 for both ends fixed
    # tagMatHinge         = 10                                # HingeMat Identifier
    # ops.uniaxialMaterial('Steel01', tagMatHinge, Mp, k_rot, 0.001)

    # ##      Link Spring Shear Material
    # tagMatSpring        = 20                                # SpringMat Identifier
    # Vp                  = 0.6*Fy*Ashear;                                print(f"Vp = {Vp:.1f} kN")
    # print(f"emax = {2*Mp/Vp*1000:.0f} mm")
    # # print(f"2.6Mp/L = {2.6*Mp/SBL:.1f} kN")
    # print(f"2.0Mp/L = {2.0*Mp/SBL:.1f} kN")
    # # print(f"1.6Mp/L = {1.6*Mp/SBL:.1f} kN")
    # k_trans             = 2*G*Ashear/SBL  
    
    # b1              = 0.003                             # Ratio of Kyield to Kelastic
    # R0,cR1,cR2      = 18.5, 0.9, 0.1                    # cR1 specifies the radius. 10<=R0<=20
    # a1= a3          = 0.06
    # a2 = a4         = 1.0
    # ops.uniaxialMaterial('Steel02', tagMatSpring, Vp, k_trans, b1, *[R0,cR1,cR2], *[a1, a2, a3, a4])
    
    # def FSF_beam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, tagMatSpring, tagMatHinge, Beams, coordsGlobal, SBL): # FBLR = Flexure Beam Length Ratio
        
    #     xI  = coordsGlobal[tagNodeI][0];    yI  = coordsGlobal[tagNodeI][1]
    #     xJ  = coordsGlobal[tagNodeJ][0];    yJ  = coordsGlobal[tagNodeJ][1]
        
    #     Lx = xJ - xI; Ly = yJ - yI
    #     L  = (Lx**2 + Ly**2)**0.5; SBLR = SBL/L
    #     FBLx = (1-SBLR)/2*Lx; FBLy = (1-SBLR)/2*Ly
        
    #     coordsLocal = {}
        
    #     tagNodeFLL = tagNodeI + 1;  coordsLocal[tagNodeFLL] = [xI, yI];                 ops.node(tagNodeFLL, *coordsLocal[tagNodeFLL])
    #     tagNodeFLR = tagNodeI + 2;  coordsLocal[tagNodeFLR] = [xI + FBLx, yI + FBLy];   ops.node(tagNodeFLR, *coordsLocal[tagNodeFLR])
    #     tagNodeSL  = tagNodeI + 3;  coordsLocal[tagNodeSL]  = [xI + FBLx, yI + FBLy];   ops.node(tagNodeSL,  *coordsLocal[tagNodeSL])
    #     tagNodeSR  = tagNodeI + 4;  coordsLocal[tagNodeSR]  = [xJ - FBLx, yJ - FBLy];   ops.node(tagNodeSR,  *coordsLocal[tagNodeSR])
    #     tagNodeFRL = tagNodeI + 5;  coordsLocal[tagNodeFRL] = [xJ - FBLx, yJ - FBLy];   ops.node(tagNodeFRL, *coordsLocal[tagNodeFRL])
    #     tagNodeFRR = tagNodeI + 6;  coordsLocal[tagNodeFRR] = [xJ, yJ];                 ops.node(tagNodeFRR, *coordsLocal[tagNodeFRR])
                
        
    #     # Rotational Spring between Wall and Left Flexure Beam
    #     ops.equalDOF(tagNodeI, tagNodeFLL, 1, 2, *[3]) 
    #     # Here you can write a spring tagMat later, BUT just do not forget to omit 3 from above equalDOF command
    #     # Flexure Beam on the Left
    #     tagElement          = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}1")
    #     Beams[tagElement]   = [tagNodeFLL, tagNodeFLR]
    #     # Translational and Rotational Springs between Shear Link and Left  Flexure Beam
    #     ops.equalDOF(tagNodeFLR, tagNodeSL, 1)
    #     tagElement          = int(f"9{tagCoordYI}{tagCoordXI}{tagCoordXJ}1")
    #     ops.element('zeroLength', tagElement, *[tagNodeFLR, tagNodeSL], '-mat', *[tagMatSpring, tagMatHinge], '-dir', *[2, 3])
    #     # Shear Link
    #     tagElement          = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}3")
    #     Beams[tagElement]   = [tagNodeSL, tagNodeSR]
    #     # Translational and Rotational Springs between Shear Link and Right Flexure Beam
    #     ops.equalDOF(tagNodeSR, tagNodeFRL, 1)  
    #     tagElement          = int(f"9{tagCoordYI}{tagCoordXI}{tagCoordXJ}2")
    #     ops.element('zeroLength', tagElement, *[tagNodeSR, tagNodeFRL], '-mat', *[tagMatSpring, tagMatHinge], '-dir', *[2, 3])
    #     # Flexure Beam on the Right
    #     tagElement          = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}2")
    #     Beams[tagElement]   = [tagNodeFRL, tagNodeFRR]
    #     # Rotational Spring between Wall and Right Flexure Beam
    #     ops.equalDOF(tagNodeFRR, tagNodeJ, 1, 2, *[3]) 
    #     # Here you can write a spring tagMat later, BUT just do not forget to omit 3 from above equalDOF command
        
    # def FSW_beam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, tagMatSpring, tagMatHinge, Beams, coordsGlobal, SBL): # FBLR = Flexure Beam Length Ratio
        
    #     xI  = coordsGlobal[tagNodeI][0];    yI  = coordsGlobal[tagNodeI][1]
    #     xJ  = coordsGlobal[tagNodeJ][0];    yJ  = coordsGlobal[tagNodeJ][1]
        
    #     Lx = xJ - xI; Ly = yJ - yI
    #     L  = (Lx**2 + Ly**2)**0.5; SBLR = SBL/L
    #     FBLx = (1-SBLR)*Lx; FBLy = (1-SBLR)*Ly
        
    #     coordsLocal = {}
        
    #     tagNodeFL = tagNodeI + 1;  coordsLocal[tagNodeFL] = [xI, yI];                   ops.node(tagNodeFL, *coordsLocal[tagNodeFL])
    #     tagNodeFR = tagNodeI + 2;  coordsLocal[tagNodeFR] = [xI + FBLx, yI + FBLy];     ops.node(tagNodeFR, *coordsLocal[tagNodeFR])
    #     tagNodeSL = tagNodeI + 3;  coordsLocal[tagNodeSL] = [xI + FBLx, yI + FBLy];     ops.node(tagNodeSL, *coordsLocal[tagNodeSL])
    #     tagNodeSR = tagNodeI + 4;  coordsLocal[tagNodeSR] = [xJ, yJ];                   ops.node(tagNodeSR, *coordsLocal[tagNodeSR])

    #     # Rotational Spring between Wall and Left Flexure Beam
    #     ops.equalDOF(tagNodeI, tagNodeFL, 1, 2, *[3]) 
    #     # Here you can write a spring tagMat later, BUT just do not forget to omit 3 from above equalDOF command
    #     # Flexure Beam on the Left
    #     tagElement          = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}1")
    #     Beams[tagElement]   = [tagNodeFL, tagNodeFR]
    #     # Translational and Rotational Springs between Shear Link and Left  Flexure Beam
    #     ops.equalDOF(tagNodeFR, tagNodeSL, 1) 
    #     tagElement          = int(f"9{tagCoordYI}{tagCoordXI}{tagCoordXJ}1")
    #     ops.element('zeroLength', tagElement, *[tagNodeFR, tagNodeSL], '-mat', *[tagMatSpring, tagMatHinge], '-dir', *[2, 3]) 
    #     # Shear Link
    #     tagElement          = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}3")
    #     Beams[tagElement]   = [tagNodeSL, tagNodeSR]
    #     # Translational and Rotational Springs between Shear Link and Right Flexure Beam
    #     ops.equalDOF(tagNodeSR, tagNodeJ, 1)
    #     tagElement          = int(f"9{tagCoordYI}{tagCoordXI}{tagCoordXJ}2")
    #     ops.element('zeroLength', tagElement, *[tagNodeSR, tagNodeJ], '-mat', *[tagMatSpring, tagMatHinge], '-dir', *[2, 3])
        # Here you can write a spring tagMat later, BUT just do not forget to omit 3 from above equalDOF command

    #   Beams and Trusses:
    ##  Define tags of  Beams and Trusses
    Beams   = {}
    Trusses = {}
    tagElementBeamHinge = []
    for tagNode, coord in coords.items():
        tagNodeI    = tagNode
        tagCoordXI  = f"{tagNodeI}"[3:-1]
        tagCoordYI  = f"{tagNodeI}"[1:-3]
        tagSuffixI  = f"{tagNodeI}"[-1]
        for tagNode, coord in coords.items():
            tagNodeJ    = tagNode
            tagCoordXJ  = f"{tagNodeJ}"[3:-1]
            tagCoordYJ  = f"{tagNodeJ}"[1:-3]
            tagSuffixJ  = f"{tagNodeJ}"[-1]
            
            if tagCoordXI != tagCoordXJ and tagCoordYI == tagCoordYJ and (tagCoordYI != '00' or tagCoordYJ != '00'):
                # build beam
                if tagCoordXJ != gridLeaningColumn:
                    if int(tagSuffixJ)-int(tagSuffixI) == -1 and int(tagCoordXJ)-int(tagCoordXI) == 1:
                        if tagSuffixI != '0' and tagSuffixJ != '0':
                            # print(f"{tagNodeI} VS {tagNodeJ} ==> tagBeam = 4{tagCoordYI}{tagCoordXI}{tagCoordXJ}")
                            if typeCB == 'discretizedAllFiber':
                                discretizeBeam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, Beams, coords, numSegBeam)
                            elif typeCB == 'FSF':
                                FSF_beam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, tagMatSpring, tagMatHinge, Beams, coords, SBL)
                            elif typeCB == 'FSW':
                                FSW_beam(tagNodeI, tagNodeJ, tagCoordYI, tagCoordXI, tagCoordXJ, tagMatSpring, tagMatHinge, Beams, coords, SBL)
                            elif typeCB == 'discritizedBothEnds':
                                # Beams[f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}"] = [tagNodeI, tagNodeJ]  #Prefix 4 is for Beams
                                tagEleBeam = int(f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}")
                                # print(f"coordNodeI = {ops.nodeCoord(tagNodeI)}")
                                # print(f"coordNodeJ = {ops.nodeCoord(tagNodeJ)}")
                                if 0:
                                    ops.equalDOF(tagNodeI, tagNodeJ, 2)
                                tagToAppend = subStructBeam(tagEleBeam, tagNodeI, tagNodeJ, tagGTLinear, beam, PHL_beam, numSegBeam, rotSpring)
                                tagElementBeamHinge.append(tagToAppend) # This function models the beams
                                print(f"tagElementBeamHinge = {tagElementBeamHinge}")
                            else: 
                                print("typeCB not recognized!"); sys.exit()
                            # Beams[f"4{tagCoordYI}{tagCoordXI}{tagCoordXJ}"] = [tagNodeI, tagNodeJ]  #Prefix 4 is for Beams
                # build truss
                elif tagCoordXJ == gridLeaningColumn and tagCoordXI == f"{(len(L_Bay_List)-2):02}":
                    if int(tagSuffixJ)-int(tagSuffixI) == -2:
                        # print(f"{tagNodeI} VS {tagNodeJ} ==> tagTruss = 2{tagCoordYI}{tagCoordXI}{tagCoordXJ}")
                        tagElement = int(f"3{tagCoordYI}{tagCoordXI}{tagCoordXJ}")
                        Trusses[tagElement] = [tagNodeI, tagNodeJ]  #Prefix 3 is for Trusses
    
    ##  Define Beams
    if typeCB == 'discretizedAllFiber':
        for tagElement, tagNodes in Beams.items():
            ops.element('dispBeamColumn',    tagElement, *tagNodes, tagGTLinear, beam.tagSec)
    elif typeCB == 'FSF' or typeCB == 'FSW':
        for tagElement, tagNodes in Beams.items():
            # print(f"tagElement = {tagElement} & tanNodes = {tagNodes}")
            tagElementSuffix = f"{tagElement}"[-1]
            if tagElementSuffix == '1' or tagElementSuffix == '2': # Flexure Beams
                # ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, 1e-4*I, tagGTLinear)
                # ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, 0.0003, tagGTLinear)
                ops.element('dispBeamColumn',    tagElement, *tagNodes, tagGTLinear, beam.tagSec)
            elif tagElementSuffix == '3': # Shear Beams 
                ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, 0.00014544948666666684, tagGTLinear)
            else:
                print("Error in defining beams!!!")
        
        
    ##  Define Trusses
    if modelLeaning == True:
        for tagElement, tagNodes in Trusses.items():
            # print(f"tagElement = {tagElement} & tanNodes = {tagNodes}")
            # ops.element('elasticBeamColumn', tagElement, *tagNodes, A, E, 1e-10*I, tagGTLinear)
            ops.element('Truss', tagElement, *tagNodes, A, tagMatTruss)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # #   Define Top-Left corner node as Control Node
    # for tagNode, coord in coords.items():
    #     tagCoordXI  = f"{tagNode}"[3:-1]
    #     tagCoordYI  = f"{tagNode}"[1:-3]
    #     tagSuffixI  = f"{tagNode}"[-1]
    #     if tagSuffixI == '0' and tagCoordXI == '00' and tagCoordYI == f"{storyNum:02}":
    #         tagNodeControl = tagNode
    #         # print(f"tagNodeControl = {tagNodeControl}")
    
    #   Define Wall Centroid Nodes of the left wall as Pushover Loading Nodes
    tagNodeControl = []
    for tagNode, coord in coords.items():
        tagCoordXI  = f"{tagNode}"[3:-1]
        tagCoordYI  = f"{tagNode}"[1:-3]
        tagSuffixI  = f"{tagNode}"[-1]
        if tagSuffixI == '0' and tagCoordXI == '00':
            tagNodeControl.append(tagNode)
            # print(f"tagNodeControl = {tagNodeControl}") 
    
    return(tagNodeControl, tagNodeBaseList, x, y, coords, wall, tagElementWallBase, beam, tagElementBeamHinge, tagNodeLoad)







