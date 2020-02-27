from snmpReportGenerator import SnmpReportGenerator
from snmpMonitorGroup import SnmpMonitorGroup
from appNewAgent import newAgent
from datetime import datetime

import appLogger
import snmpQuery
import time
import sys
import re

OPTION_MIN = 0
OPTION_MAX = 4
SLEEP_TIME = 1 

def selectAgent(agentList):
    if len(agentList) == 0:
        print('No hay agentes disponibles.')
        return None

    optionMin, optionMax = 0, len(agentList)
    pattern = re.compile('^\d+$')

    print('Agentes disponibles:')
    for x in range(optionMin, optionMax):
        print('\t', x, ' ', agentList[x])
    print()

    while True:
        selected = input('Ingresa el indice del agente: ')
        selected = selected.strip()
        if not selected:
            print('Por favor ingresa un indice.')
            continue
        if not pattern.match(selected):
            print('Solo puedes ingresar indices de la lista.')
            continue
        selected = int(selected)
        if selected < optionMin or optionMax < selected:
            print('Ingresa solo indices de la lista.')
            continue        
        return agentList[selected]

def showMenu():
    print()
    print('Monitoreo SNMP, selecciona tu opcion.')
    print('[0] Salir.')
    print('[1] Resumen General.')
    print('[2] Agregar Agente.')
    print('[3] Eliminar Agente.')
    print('[4] Generar Reporte.')
    print()

    pattern = re.compile('^\d$')

    while True:
        option = input('Ingresa una opcion: ').strip()
        if not option:
            continue
        if not pattern.match(option):
            print('Ingresa un numero que represente la opcion.')
            continue
        option = int(option)
        if option < OPTION_MIN or OPTION_MAX < option:
            print('Ingresa solo elementos de la lista.')
            continue
        return option

def getDatetime():
    pattern = re.compile('^\d{4}\s+\d{2}\s+\d{2}\s+\d{2}\s+\d{2}\s+\d{2}$')
    
    while True:
        date = input('Ingresa la fecha y hora en el formato YYYY MM DD HH mm SS : ')
        date = date.strip()
        if not date:
            print('Por favor ingresa una fecha y hora.')
            continue
        if not pattern.match(date):
            print('Ingresa la fecha y hora en el programa especificado.')
            continue
        try:
            tokens = list(map(lambda x : int(x), date.split()))
            date = datetime(tokens[0], tokens[1], tokens[2],
                tokens[3], tokens[4], tokens[5])
        except ValueError:
            print('Revisa la fecha y hora.')
            continue
        epoch = datetime.fromtimestamp(0)
        if date < epoch: 
            print('La fecha y hora deben ser despues de ', epoch)
            continue
        return date

if __name__ == '__main__':

    appLogger.configureLogger()

    monitorGroup = SnmpMonitorGroup()

    while True:
        time.sleep(SLEEP_TIME)
        option = showMenu()
        
        if option == 0:

            del monitorGroup
            sys.exit(0)

        elif option == 1:

            print('* meow meow meow *')

        elif option == 2:

            agentInfo = newAgent()
            if agentInfo:
                monitorGroup.addAgentMonitor(agentInfo)

        elif option == 3:

            agentInfo = selectAgent(monitorGroup.agents)
            if agentInfo:
                monitorGroup.removeAgentMonitor(agentInfo)

        elif option == 4:
    
            agentInfo = selectAgent(monitorGroup.agents)
            if not agentInfo:
                continue

            print('Ingresa la fecha y hora de inicio:')
            startTime = int(getDatetime().timestamp())
            print('Ingresa la fecha y hora de fin:')
            endTime = int(getDatetime().timestamp())

            if startTime > endTime:
                swapTime = endTime
                endTime = startTime
                startTime = swapTime

            print('Generando reporte...')
            pdfMaker = SnmpReportGenerator(agentInfo)
            pdfMaker.makeReport(startTime, endTime)

        else:
            continue
