import rrdConstants
import rrdtool

def makeNetworkGraph(root, startTime, endTime = rrdConstants.NOW):

    return rrdtool.graphv(root + '/' + rrdConstants.NETWORK_GRAPH,
            '--imgformat', 'PDF',
            '--start', startTime,
            '--end', endTime,
            
            '--width', rrdConstants.GRAPH_WIDTH,
            '--height', rrdConstants.GRAPH_HEIGHT,
            '--full-size-mode',

            '--title', 'Ancho de Banda de Entrada',
            '--vertical-label', 'bits/s',

            'DEF:data=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':AVERAGE',
            'DEF:pred=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':HWPREDICT',
            'DEF:dev=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':DEVPREDICT',
            'DEF:fail=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':FAILURES',

            'VDEF:last=fail,LAST',

            'CDEF:upper=pred,dev,2,*,+',
            'CDEF:lower=pred,dev,2,*,-',

#            'TICK:fail#F4433666:1.0:  Fallos',
            'LINE2:data#64DD17:Ancho de Banda Promedio',
#            'LINE1:upper#D50000:Limite Superior',
#            'LINE1:lower#0091EA:Limite Inferior',

            'PRINT:last:%1.0lf'
        )['print[0]']

