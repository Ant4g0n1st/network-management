import rrdConstants

def BuildDataSourceString(sourceName, typeName, 
    threshold = rrdConstants.THRESHOLD,
    sampleMin = rrdConstants.UNKNOWN,
    sampleMax = rrdConstants.UNKNOWN):

    return 'DS:{0}:{1}:{2}:{3}:{4}'.format(sourceName, 
        typeName, threshold, sampleMin, sampleMax)

