exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open(f"Input/units{'US'}.py").read())


# import sys
import openseespy.opensees        as ops
import functions.FuncMaterial     as fmat
import opsvis                     as opv
import matplotlib.pyplot          as plt

def makeSectionRect(tagSec, H, B, definedMatList, typeMatSt='ReinforcingSteel', NfibeY=120, NfibeZ=1):
    
    GJ = 1e6
    # Section Geometry
    
    crdsI = [-H/2, -B/2]
    crdsJ = [ H/2,  B/2]
    
    # Steel Material
    tagMatSt        = 1
    typeMat         = 'Steel02' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    if tagMatSt not in definedMatList:
        fmat.matSteel(typeMat, tagMatSt)
        definedMatList.append(tagMatSt)
    
    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt, NfibeY, NfibeZ, *crdsI, *crdsJ)
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt, NfibeY, NfibeZ, *crdsI, *crdsJ]
             ]
             
    return fib_sec

def makeSectionI(tagSec, Hw, Bf, tw, tf, definedMatList, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
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
    typeMat         = 'Steel02' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    if tagMatSt not in definedMatList:
        fmat.matSteel(typeMat, tagMatSt)
        definedMatList.append(tagMatSt)
        
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

def makeSectionBox(tagSec, Hw, Bf, tw, tf, tc, definedMatList, typeMatSt='ReinforcingSteel', NfibeY=40, NfibeZ=1):
    
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
    if tagMatSt not in definedMatList:
        fmat.matSteel(typeMat, tagMatSt)
        definedMatList.append(tagMatSt)
    
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

def makeSectionBoxComposite(section, NfibeZ=1):
    tagSec      = section.tagSec        ; print(f"tagSec    = {tagSec   }")
    tagMatSt2   = section.tagMatStFlange; print(f"tagMatSt2 = {tagMatSt2}")
    tagMatSt1   = section.tagMatStWeb   ; print(f"tagMatSt1 = {tagMatSt1}")
    tagMatCt1   = section.tagMatCtUnconf; print(f"tagMatCt1 = {tagMatCt1}")
    tagMatCt2   = section.tagMatCtConf  ; print(f"tagMatCt2 = {tagMatCt2}")
    tw          = section.tw            ; print(f"tw        = {tw       }")
    Hw          = section.Hw            ; print(f"Hw        = {Hw       }")
    tf          = section.tf            ; print(f"tf        = {tf       }")
    Bf          = section.Bf            ; print(f"Bf        = {Bf       }")
    tc          = section.tc            ; print(f"tc        = {tc       }")
    Hc1         = section.Hc1           ; print(f"Hc1       = {Hc1      }")
    NfibeY      = section.NfibeY        ; print(f"NfibeY    = {NfibeY   }")

    
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
    
    # #  Material
    # ## Steel Material 1
    # tagMatSt1       = 1
    # typeMat         = 'ReinforcingSteel' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    # if tagMatSt1 not in definedMatList:
    #     fmat.matSteel(typeMat, tagMatSt1)
    #     definedMatList.append(tagMatSt1)
    # ## Steel Material 2
    # tagMatSt2       = 2
    # typeMat         = 'ReinforcingSteel' # Elastic, ElasticPP, Steel02, ReinforcingSteel
    # if tagMatSt2 not in definedMatList:
    #     fmat.matSteel(typeMat, tagMatSt2)
    #     definedMatList.append(tagMatSt2)
    
    # ## Unconfined Concrete Material
    # tagMatCt1        = 3
    # typeMat         = 'Concrete02' # Elastic, ElasticPP, Concrete02
    # if tagMatCt1 not in definedMatList:
    #     fmat.matConcrete(typeMat, tagMatCt1)
    #     definedMatList.append(tagMatCt1)
    # ## Confined Concrete Material
    # tagMatCt2        = 4
    # typeMat         = 'Concrete02' # Elastic, ElasticPP, Concrete02
    # if tagMatCt2 not in definedMatList:
    #     fmat.matConcrete(typeMat, tagMatCt2)
    #     definedMatList.append(tagMatCt2)

    # Define Sections
    #        section('Fiber', tagSec, '-GJ', GJ)
    ops.section('Fiber', section.tagSec, '-GJ', GJ)
    ops.patch('rect', tagMatSt2, NfibeY,        NfibeZ, *crdsI1, *crdsJ1) #Bot Flange
    ops.patch('rect', tagMatSt2, NfibeY,        NfibeZ, *crdsI4, *crdsJ4) #Top Flange
    ops.patch('rect', tagMatSt1, NfibeY*times,  NfibeZ, *crdsI2, *crdsJ2) #Left Web
    ops.patch('rect', tagMatSt1, NfibeY*times,  NfibeZ, *crdsI3, *crdsJ3) #Right Web
    ops.patch('rect', tagMatCt2, NfibeY*times2, NfibeZ, *crdsI5, *crdsJ5) #Concrete Core bot
    ops.patch('rect', tagMatCt1, NfibeY*times1, NfibeZ, *crdsI6, *crdsJ6) #Concrete Core mid
    ops.patch('rect', tagMatCt2, NfibeY*times2, NfibeZ, *crdsI7, *crdsJ7) #Concrete Core top
    
    
    # this part of the code is just to sent out a varibale for plotting the fiber section
    fib_sec = [['section', 'Fiber', tagSec, '-GJ', GJ],

             ['patch', 'rect', tagMatSt2, NfibeY,        NfibeZ, *crdsI1, *crdsJ1], #Bot Flange
             ['patch', 'rect', tagMatSt2, NfibeY,        NfibeZ, *crdsI4, *crdsJ4], #Top Flange
             ['patch', 'rect', tagMatSt1, NfibeY*times,  NfibeZ, *crdsI2, *crdsJ2], #Left Web
             ['patch', 'rect', tagMatSt1, NfibeY*times,  NfibeZ, *crdsI3, *crdsJ3], #Right Web
             ['patch', 'rect', tagMatCt2, NfibeY*times2, NfibeZ, *crdsI5, *crdsJ5],  #Concrete Core bot
             ['patch', 'rect', tagMatCt1, NfibeY*times1, NfibeZ, *crdsI6, *crdsJ6],  #Concrete Core mid
             ['patch', 'rect', tagMatCt2, NfibeY*times2, NfibeZ, *crdsI7, *crdsJ7],  #Concrete Core top
             ]
    # matcolor = ['y', 'b', 'r', 'g', 'm', 'k']
    # # matcolor = ['r', 'lightgrey', 'pink', 'gold', 'purple', 'orange', 'w']
    # opv.plot_fiber_section(fib_sec, matcolor=matcolor)
    # plt.axis('equal')
    # # plt.savefig('fibsec_rc.png')
    
    # plt.show()
    return fib_sec





























