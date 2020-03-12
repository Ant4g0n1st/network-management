DS_MEMORY = 'memory'
DS_DISK = 'disk'
DS_CPU = 'cpu'

TYPE_COUNTER = 'COUNTER'
TYPE_GAUGE = 'GAUGE'

# 5-minute frequency is recommended.
THRESHOLD = '60'
STEP = '30'

# Let's collect five hours.
RRA_DEFAULT_SETTINGS = 'RRA:AVERAGE:0.5:1:60'

UNKNOWN = 'U'
NOW = 'N'

GRAPH_HEIGHT = '320'
GRAPH_WIDTH = '1280'

MEMORY_GRAPH = 'memory.png'
DISK_GRAPH = 'disk.png'
CPU_GRAPH = 'cpu.png'

TIME_FRAME = 1200

# Baseline levels
NO_ALERT = 0
READY = 10
SET = 20
GO = 30

# Actual baseline
BASELINE = {
        DS_MEMORY : { READY : 60, SET : 70, GO : 85},
        DS_DISK : { READY : 25, SET : 40, GO : 50},
        DS_CPU : { READY : 60, SET : 75, GO : 90}
    }
