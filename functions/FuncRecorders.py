import openseespy.opensees as ops




def recordPushover(tagNodeControl, tagNodeBase, outputDir):
    
    #   recorder('Node', '-file', filename,                        '-time', '-node', *nodeTags=[], '-dof', *dofs=[], respType)
    ops.recorder('Node', '-file', f"{outputDir}/top_disp.txt",     '-time', '-node', tagNodeControl,  '-dof', 1,        'disp')
    if type(tagNodeBase) == list:
        ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node', *tagNodeBase,     '-dof', 1,        'reaction')
    else: 
        ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node',  tagNodeBase,     '-dof', 1,        'reaction')

def recordStressStrain(outputDir, tagEleList, fiberMat, section, H, tf, NfibeY):
    
    # coords_Fiber:
    coordsFiber         = {}
    ## top
    coordsFiber['top']  = [ (H/2 - tf/(2*NfibeY)), 0]
    ## bot
    coordsFiber['bot']  = [-(H/2 - tf/(2*NfibeY)), 0]
    ## mid
    coordsFiber['mid']  = [ 0                    , 0.001]

    #   recorder('Element', '-file', filename,                          '-ele', *eleTags=[], *args)
    #                                                                                        *args for dispBeamColumn elements are  when creating an ElementRecorder object are 'force,' and 'section $secNum secArg1 secArg2...'
    #                                                                                        'section $secNum secArg1 secArg2...'  Where $secNum refers to the integration point whose data is to be output valid entries being 1 through $numIntgrPts.
    #                                                                                                         'fiber', y, z,                tagMat, 'stressStrain'        #(It can also be used as 'fiber', y, z, tagMat, 'stressStrain' so as to record the closest fiber to [y,z] with material tag tagMat)
    ##  Top Flange
    ops.recorder('Element', '-file', f"{outputDir}/fiberSt_top.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['top'], section.tagMatStFlange, 'stressStrain')
    ##  Bottom Flange
    ops.recorder('Element', '-file', f"{outputDir}/fiberSt_bot.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['bot'], section.tagMatStFlange, 'stressStrain')
    ##  Mid Web
    ops.recorder('Element', '-file', f"{outputDir}/fiberSt_mid.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['mid'], section.tagMatStWeb, 'stressStrain')
    ##  Top Confined Concrete
    ops.recorder('Element', '-file', f"{outputDir}/fiberCt2_top.txt", '-ele', *tagEleList,           
                  'section', section.tagSec,    'fiber', *coordsFiber['top'], section.tagMatCtConf, 'stressStrain')
    ##  Bottom Confined Concrete
    ops.recorder('Element', '-file', f"{outputDir}/fiberCt2_bot.txt", '-ele', *tagEleList,           
                  'section', section.tagSec,    'fiber', *coordsFiber['bot'], section.tagMatCtConf, 'stressStrain')
    ##  Top Unconfined Concrete
    ops.recorder('Element', '-file', f"{outputDir}/fiberCt1_top.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['top'], section.tagMatCtUnconf, 'stressStrain')
    ##  Bottom Unconfined Concrete
    ops.recorder('Element', '-file', f"{outputDir}/fiberCt1_bot.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['bot'], section.tagMatCtUnconf, 'stressStrain')
    ##  Mid Unconfined Concrete
    ops.recorder('Element', '-file', f"{outputDir}/fiberCt1_mid.txt", '-ele', *tagEleList,           
                 'section', section.tagSec,    'fiber', *coordsFiber['mid'], section.tagMatCtUnconf, 'stressStrain')
    
    return(coordsFiber)
    





































