import appConstants
import rrdConstants
import rrdtool

def makeCPUGraph(root, startTime, endTime = rrdConstants.NOW):

    rrdtool.graphv(root + '/' + rrdConstants.CPU_GRAPH,
            '--start', startTime,
            '--end', endTime,
            
            '--width', rrdConstants.GRAPH_WIDTH,
            '--height', rrdConstants.GRAPH_HEIGHT,
            '--full-size-mode',

            '--title', 'Porcentaje de uso de procesador',
            '--vertical-label', '% CPU',
            '--lower-limit', '0',
            '--upper-limit', '100',

            # Get the processor load.
            'DEF:data=' + root + '/' + appConstants.DB_FILENAME + ':' + rrdConstants.DS_CPU + ':AVERAGE',

            # Compute Least Squares Line slope.
            'VDEF:predSlope=data,LSLSLOPE',
        
            # Compute Least Squares Line y-intercept.
            'VDEF:predInt=data,LSLINT',

            # Compute average processor load.
            'VDEF:avg=data,AVERAGE',

            # Compute the values for the Least Squares Line.
            'CDEF:predLine=data,POP,COUNT,predSlope,*,predInt,+',

            # Compute the predicted values above 90%
            'CDEF:overNinety=predLine,90,GE,predLine,UNKN,IF',
            
            # Compute the predicted values above 99%
            'CDEF:reachedHundred=predLine,99,GT,predLine,UNKN,IF',

            # Get the first value to print the timestamp in the graph.
            'VDEF:firstNinety=overNinety,FIRST',
            'VDEF:firstHundred=reachedHundred,FIRST',

            'CDEF:predicted=predLine,0,100,LIMIT',
            'CDEF:predictedOverNinety=predicted,90,GE,predicted,0,IF',

            'AREA:predictedOverNinety#B3E5FC',
            'AREA:data#0091EA:% Carga CPU',
            'HRULE:avg#33691E:Carga CPU Promedio:dashes=3',
            'LINE3:predicted#FF1744:Prediccion:dashes=3',
            'AREA:90',
            'AREA:5#FF8A8077:STACK',
            'AREA:5#FF174477:STACK',

            # Print the timestamps in the graph.
            'GPRINT:firstNinety:Alcanzara 90%% el %d de %B de %Y a las %H\:%M\:%S:strftime',
            'GPRINT:firstHundred:Alcanzara 100%% el %d de %B de %Y a las %H\:%M\:%S:strftime',
            
        )

def makeNetworkGraph(root, startTime, endTime = rrdConstants.NOW):

    shift = int(rrdConstants.HW_PERIOD) * int(rrdConstants.STEP)

    shiftedStart = int(startTime) - shift
    shiftedEnd = int(endTime) - shift
    
    shiftedStart = str(shiftedStart)
    shiftedEnd = str(shiftedEnd)
    shift = str(shift)

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
            'DEF:prev=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':AVERAGE:start=' + shiftedStart + ':end=' + shiftedEnd,
            'DEF:pred=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':HWPREDICT',
            'DEF:dev=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':DEVPREDICT',
            'DEF:fail=' + root + '/' + rrdConstants.HW_FILENAME + ':' + rrdConstants.DS_NETWORK + ':FAILURES',

            'VDEF:last=fail,LAST',
            'VDEF:maxDev=dev,MAXIMUM',

            'CDEF:upper=pred,dev,2,*,+',
            'CDEF:lower=pred,dev,2,*,-',
            'CDEF:printDev=dev,maxDev,-',

            'VDEF:firstData=data,FIRST',
            'VDEF:lastData=data,LAST',

            'GPRINT:firstData:Desde %d/%m/%Y %H\:%M\:%S:strftime',
            'GPRINT:lastData:Hasta %d/%m/%Y %H\:%M\:%S\c:strftime',

            'TICK:fail#FFEB3B:1.0:  Fallos\c',

            'SHIFT:prev:' + shift,
            'AREA:prev#e0e0e0CC:Periodo Anterior\t',

            'VDEF:totalPrev=prev,TOTAL',
            'VDEF:maxPrev=prev,MAXIMUM',
            'VDEF:avgPrev=prev,AVERAGE',

            'GPRINT:totalPrev:Total\:\t%0.3lf%s',
            'GPRINT:maxPrev:Máximo\:\t%0.3lf%s',
            'GPRINT:avgPrev:Promedio\: %0.3lf%s\c',

            'LINE2:data#0091EA:Ancho de Banda\t',

            'VDEF:totalData=data,TOTAL',
            'VDEF:maxData=data,MAXIMUM',
            'VDEF:avgData=data,AVERAGE',

            'GPRINT:totalData:Total\:\t%0.3lf%s',
            'GPRINT:maxData:Máximo\:\t%0.3lf%s',
            'GPRINT:avgData:Promedio\: %0.3lf%s\c',

            'LINE2:pred#FF4081:Predicción',
            'LINE1:upper#D50000:Límite Superior',
            'LINE1:lower#64DD17:Límite Inferior',
            'LINE1:printDev#000000:Desviación\c',

            'PRINT:last:%1.0lf'
        )['print[0]']

