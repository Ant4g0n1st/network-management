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

            '--title', 'Porcentaje de uso de procesador.',
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
            'GPRINT:firstNinety:Alcanzara 90%% el %d de %B de %Y a las %H\:%M\:%s:strftime',
            'GPRINT:firstHundred:Alcanzara 100%% el %d de %B de %Y a las %H\:%M\:%s:strftime',
            
        )

