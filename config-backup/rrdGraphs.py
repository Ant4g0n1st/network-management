import appConstants
import rrdConstants
import rrdtool

def makeMemoryGraph(root, startTime, endTime = rrdConstants.NOW):
    rrdtool.graph(root + '/' + rrdConstants.MEMORY_GRAPH,
            '--start', startTime,
            '--end', endTime,
            
            '--width', rrdConstants.GRAPH_WIDTH,
            '--height', rrdConstants.GRAPH_HEIGHT,
            '--full-size-mode',

            '--title', 'Porcentage de uso de memoria.',
            '--vertical-label', '% Memoria',
            '--lower-limit', '0',
            '--upper-limit', '100',

            'DEF:data=' + root + '/' + appConstants.DB_FILENAME + ':' + rrdConstants.DS_MEMORY + ':AVERAGE',

            'AREA:data#D4E157:% Memoria utilizada'
        )

def makeDiskGraph(root, startTime, endTime = rrdConstants.NOW):
    rrdtool.graph(root + '/' + rrdConstants.DISK_GRAPH,
            '--start', startTime,
            '--end', endTime,
            
            '--width', rrdConstants.GRAPH_WIDTH,
            '--height', rrdConstants.GRAPH_HEIGHT,
            '--full-size-mode',

            '--title', 'Porcentage de uso de Disco.',
            '--vertical-label', '% Disco',
            '--lower-limit', '0',
            '--upper-limit', '100',

            'DEF:data=' + root + '/' + appConstants.DB_FILENAME + ':' + rrdConstants.DS_DISK + ':AVERAGE',

            'AREA:data#D4E157:% Disco utilizado'
        )

def makeCPUGraph(root, startTime, endTime = rrdConstants.NOW):
    rrdtool.graph(root + '/' + rrdConstants.CPU_GRAPH,
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

            'AREA:data#D4E157:% Carga CPU Promedio'
        )

