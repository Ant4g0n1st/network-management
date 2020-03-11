import rrdtool

OUTPUT = 'stats.png'
INPUT = 'udp.rrd'

begin = rrdtool.last(INPUT) - 1350

rrdtool.graph(OUTPUT,
        '--start', str(begin),
        '--end', 'N',

        '--title', 'Comportamiento de los Datagramas UDP',
        '--vertical-label', 'Datagramas UDP',
        '--width', '1280',
        '--height', '320',
        '--full-size-mode',

        'DEF:in=' + INPUT + ':udpIn:AVERAGE',
        'DEF:out=' + INPUT + ':udpOut:AVERAGE',

        # Uso de suma para obtener el total.
        'CDEF:all=in,out,+',
        # Division y multiplicacion para obtener
        # porcentage de entrada.
        'CDEF:inp=in,all,/,100,*',
        # Division y multiplicacion para obtener
        # porcentage de salida.
        'CDEF:outp=out,all,/,100,*',
        # Comparacion para saber si domina
        # la entrada.
        'CDEF:bigin=inp,outp,GT,INF,0,IF',
        # Comparacion para saber si domina
        # la salida.
        'CDEF:bigout=outp,inp,LT,0,INF,IF',
        # Comparacion para saber si son
        # muy semejantes.
        'CDEF:equal=outp,inp,-,ABS,0.001,LT,INF,0,IF',

        'AREA:bigin#555555:Mayoria In',
        'AREA:bigout#333333:Mayoria Out',
        'AREA:equal#444444:Semejantes',
        'LINE3:in#FF0000:Datagramas UDP In',
        'LINE3:out#0000FF:Datagramas UDP Out',
    )

