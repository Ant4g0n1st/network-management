import appConstants
import rrdConstants
import rrdtool

def makeCPUGraph(root, startTime, endTime = rrdConstants.NOW):

    return rrdtool.graphv(root + '/' + rrdConstants.CPU_GRAPH,
            '--start', startTime,
            '--end', endTime,
            
            '--width', rrdConstants.GRAPH_WIDTH,
            '--height', rrdConstants.GRAPH_HEIGHT,
            '--full-size-mode',

            '--title', 'Porcentage de uso de procesador.',
            '--vertical-label', '% CPU',
            '--lower-limit', '0',
            '--upper-limit', '100',

            'DEF:data=' + root + '/' + appConstants.DB_FILENAME + ':' + rrdConstants.DS_CPU + ':AVERAGE',
            'CDEF:ready=data,' + str(baseline[rrdConstants.READY]) + ',GT,data,0,IF',
            'CDEF:set=data,' + str(baseline[rrdConstants.SET]) + ',GT,data,0,IF',
            'CDEF:go=data,' + str(baseline[rrdConstants.GO]) + ',GT,data,0,IF',

            'VDEF:last=data,LAST',

            'AREA:data#D4E157:% Carga CPU Promedio',
            'AREA:ready#42A5F5:Ready',
            'AREA:set#FFEE58:Set',
            'AREA:go#EF5350:Go',

            'HRULE:' + str(baseline[rrdConstants.READY]) + '#2979FF',
            'HRULE:' + str(baseline[rrdConstants.SET]) + '#FFEA00',
            'HRULE:' + str(baseline[rrdConstants.GO]) + '#FF1744',

            'PRINT:last:%6.2lf'
        )['print[0]']

