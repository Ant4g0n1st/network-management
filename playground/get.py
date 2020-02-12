import pysnmp.hlapi as Snmp

errorIndication, errorStatus, errorIndex, varBinds = next(
    Snmp.getCmd(
        Snmp.SnmpEngine(),
        Snmp.CommunityData('grupo4cv5'),
        Snmp.UdpTransportTarget(('127.0.0.1', 161)),
        Snmp.ContextData(),
        Snmp.ObjectType(Snmp.ObjectIdentity('1.3.6.1.2.1.1.1.0'))
    )
)

# Missing error checks.
for name, value in varBinds:
    print('Object Name :', name)
    print('Object Value :', value)

