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

def makeSectionI(tagSec, H, B, tw, tf, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    
    crdsI1 = [-H/2,      -B/2 ]
    crdsJ1 = [-H/2 + tf,  B/2 ]
    
    crdsI3 = [ H/2 - tf, -B/2 ]
    crdsJ3 = [ H/2     ,  B/2 ]
    
    crdsI2 = [-H/2 + tf, -tw/2]
    crdsJ2 = [ H/2 - tf,  tw/2]
    
    times  = int(H/tf/10)
    
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

def makeSectionBox(tagSec, H, B, tw, tf, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    
    crdsI1 = [-H/2,      -B/2       ]
    crdsJ1 = [-H/2 + tf,  B/2       ]
    
    crdsI4 = [ H/2 - tf, -B/2       ]
    crdsJ4 = [ H/2     ,  B/2       ]
    
    crdsI2 = [-H/2 + tf, -B/2       ]
    crdsJ2 = [ H/2 - tf, -B/2 + tw  ]
    
    crdsI3 = [-H/2 + tf,  B/2 - tw  ]
    crdsJ3 = [ H/2 - tf,  B/2       ]
    
    times  = int(H/tf/10)
    
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

def makeSectionBoxComposite(tagSec, H, B, tw, tf, typeMatSt='ReinforcingSteel', typeMatCt='Concrete02', NfibeY=40, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    
    crdsI1 = [-H/2,      -B/2       ]
    crdsJ1 = [-H/2 + tf,  B/2       ]
    
    crdsI4 = [ H/2 - tf, -B/2       ]
    crdsJ4 = [ H/2     ,  B/2       ]
    
    crdsI2 = [-H/2 + tf, -B/2       ]
    crdsJ2 = [ H/2 - tf, -B/2 + tw  ]
    
    crdsI3 = [-H/2 + tf,  B/2 - tw  ]
    crdsJ3 = [ H/2 - tf,  B/2       ]
    
    crdsI5 = [-H/2 + tf, -B/2 + tw  ]
    crdsJ5 = [ H/2 - tf,  B/2 - tw  ]
    
    times  = int(H/tf/10)
    
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





























