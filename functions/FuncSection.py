# exec(open("functions/units.py").read())
exec(open("functions/unitsUS.py").read())


# import sys
import openseespy.opensees        as ops
import functions.FuncMaterial     as fmat

def makeSectionRect(tagSec, H, B, typeMatSt='ReinforcingSteel', NfibeY=120, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    
    crdsI = [-H/2, -B/2]
    crdsJ = [ H/2,  B/2]
    
    
    # Steel Material
    tagMatSt        = 1
    typeMat         = 'Steel02'
    fmat.matSteel(typeMat, tagMatSt)
    
    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt, NfibeY, NfibeZ, *crdsI, *crdsJ)
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt, NfibeY, NfibeZ, *crdsI, *crdsJ]
             ]
             
    return fib_sec

def makeSectionI(tagSec, Hw, Bf, tw, tf, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    ##  Bottom Flange
    crdsI1 = [-(Hw/2 + tf), -Bf/2]
    crdsJ1 = [- Hw/2      ,  Bf/2]
    ##  Top Flange
    crdsI3 = [  Hw/2      , -Bf/2]
    crdsJ3 = [ (Hw/2 + tf),  Bf/2]
    ##  Web
    crdsI2 = [-Hw/2       , -tw/2]
    crdsJ2 = [ Hw/2       ,  tw/2]
    
    times  = int(Hw/tf/10)
    
    # Steel Material
    tagMatSt        = 1
    typeMat         = 'Steel02'
    fmat.matSteel(typeMat, tagMatSt)
    
    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1) #Bot Flange
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI3, *crdsJ3) #Top Flange
    ops.patch('rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2) #Web
    
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1], #Bot Flange
             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI3, *crdsJ3], #Top Flange
             ['patch', 'rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2]  #Web
             ]
    
    return fib_sec

def makeSectionBox(tagSec, Hw, Bf, tw, tf, tc, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
    GJ = 1e6
    #   Section Geometry
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
    
    times  = int(Hw/tf/10)
    
    # Steel Material
    tagMatSt        = 1
    typeMat         = 'ReinforcingSteel' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    fmat.matSteel(typeMat, tagMatSt)
    
    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1) #Bot Flange
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI4, *crdsJ4) #Top Flange
    ops.patch('rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2) #Left Web
    ops.patch('rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI3, *crdsJ3) #Right Web
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1], #Bot Flange
             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI4, *crdsJ4], #Top Flange
             ['patch', 'rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2], #Left Web
             ['patch', 'rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI3, *crdsJ3]  #Right Web
             ]
    
    return fib_sec

def makeSectionBoxComposite(tagSec, Hw, Bf, tw, tf, tc, typeMatSt='ReinforcingSteel', typeMatCt='Concrete02', NfibeY=40, NfibeZ=1):
    
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
    ##  Concrete Core
    crdsI5 = [-Hw/2       , -tc/2       ]
    crdsJ5 = [ Hw/2       ,  tc/2       ]
    
    times  = int(Hw/tf/10)
    
    #  Material
    ## Steel Material
    tagMatSt        = 1
    typeMat         = 'ReinforcingSteel' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    fmat.matSteel(typeMat, tagMatSt)
    
    ## Concrete Material
    tagMatCt        = 2
    typeMat         = 'Concrete02' # Elastic, ElasticPP, Concrete02
    fmat.matConcrete(typeMat, tagMatCt)
    
    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1) #Bot Flange
    ops.patch('rect', tagMatSt, NfibeY,       NfibeZ, *crdsI4, *crdsJ4) #Top Flange
    ops.patch('rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2) #Left Web
    ops.patch('rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI3, *crdsJ3) #Right Web
    ops.patch('rect', tagMatCt, NfibeY*times, NfibeZ, *crdsI5, *crdsJ5) #Concrete Core
    
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI1, *crdsJ1], #Bot Flange
             ['patch', 'rect', tagMatSt, NfibeY,       NfibeZ, *crdsI4, *crdsJ4], #Top Flange
             ['patch', 'rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI2, *crdsJ2], #Left Web
             ['patch', 'rect', tagMatSt, NfibeY*times, NfibeZ, *crdsI3, *crdsJ3], #Right Web
             ['patch', 'rect', tagMatCt, NfibeY*times, NfibeZ, *crdsI5, *crdsJ5]  #Concrete Core
             ]
    
    return fib_sec





























