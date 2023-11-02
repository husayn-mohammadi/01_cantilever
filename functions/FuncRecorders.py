import openseespy.opensees as ops




def recordPushover(tagNodeControl, tagNodeBase, outputDir):
    
    #   recorder('Node', '-file', filename,                        '-time', '-node', *nodeTags=[], '-dof', *dofs=[], respType)
    ops.recorder('Node', '-file', f"{outputDir}/top_disp.txt",     '-time', '-node', tagNodeControl,  '-dof', 1,        'disp')
    if type(tagNodeBase) == list:
        ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node', *tagNodeBase,     '-dof', 1,        'reaction')
    else: 
        ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node',  tagNodeBase,     '-dof', 1,        'reaction')

def recordStressStrain(outputDir, tagEle, fiberMat, tagMat, H, tf, NfibeY):
    
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
    ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_top.txt", '-ele', *tagEle,           'section', 1,    'fiber', *coordsFiber['top'], tagMat, 'stressStrain')
    ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_bot.txt", '-ele', *tagEle,           'section', 1,    'fiber', *coordsFiber['bot'], tagMat, 'stressStrain')
    if fiberMat == "fiberSt":
        ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_mid.txt", '-ele', *tagEle,       'section', 1,    'fiber', *coordsFiber['mid'], 2, 'stressStrain')
    elif fiberMat == "fiberCt1" or fiberMat == "fiberCt2":
        ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_mid.txt", '-ele', *tagEle,       'section', 1,    'fiber', *coordsFiber['mid'], 3, 'stressStrain')
    return(coordsFiber)
    





































