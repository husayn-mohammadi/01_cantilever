import openseespy.opensees as ops




def recordPushover(ControlNode, BaseNode, outputDir):
    
    #   recorder('Node', '-file', filename,                    '-time', '-node', *nodeTags=[], '-dof', *dofs=[], respType)
    ops.recorder('Node', '-file', f"{outputDir}/top_disp.txt", '-time', '-node', ControlNode,  '-dof', 1,        'disp')
    ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node', BaseNode,     '-dof', 1,        'reaction')

def recordStressStrain(outputDir, fiberMat, tagMat, H, tf, NfibeY):
    
    # coords_Fiber:
    coordsFiber         = {}
    ## top
    coordsFiber['top']  = [ (H/2 - tf/(2*NfibeY)), 0]
    ## bot
    coordsFiber['bot']  = [-(H/2 - tf/(2*NfibeY)), 0]

    #   recorder('Element', '-file', filename,                          '-ele', *eleTags=[], *args)
    #                                                                                        *args for dispBeamColumn elements are  when creating an ElementRecorder object are 'force,' and 'section $secNum secArg1 secArg2...'
    #                                                                                        'section $secNum secArg1 secArg2...'  Where $secNum refers to the integration point whose data is to be output valid entries being 1 through $numIntgrPts.
    #                                                                                                         'fiber', y, z,                tagMat, 'stressStrain'        #(It can also be used as 'fiber', y, z, tagMat, 'stressStrain' so as to record the closest fiber to [y,z] with material tag tagMat)
    ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_top.txt", '-ele', 1,           'section', 1,    'fiber', *coordsFiber['top'], tagMat, 'stressStrain')
    ops.recorder('Element', '-file', f"{outputDir}/{fiberMat}_bot.txt", '-ele', 1,           'section', 1,    'fiber', *coordsFiber['bot'], tagMat, 'stressStrain')
    return(coordsFiber)
    





































