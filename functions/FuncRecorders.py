import openseespy.opensees as ops




def getPushoverRecorders(ControlNode, outputDir):
    
    #   recorder('Node', '-file', filename, '-xml', filename, '-binary', filename, '-tcp', inetAddress, port, '-precision', nSD=6, '-timeSeries', tsTag, '-time', '-dT', deltaT=0.0, '-closeOnWrite', '-node', *nodeTags=[], '-nodeRange', startNode, endNode, '-region', regionTag, '-dof', *dofs=[], respType)
    ops.recorder('Node', '-file', f"{outputDir}/top_disp.txt", '-time', '-node', ControlNode,'-dof', 1, 'disp')
    ops.recorder('Node', '-file', f"{outputDir}/reaction.txt", '-time', '-node', 1,          '-dof', 1, 'reaction')









































