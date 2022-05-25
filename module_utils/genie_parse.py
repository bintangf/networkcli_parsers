import paramiko, json
from genie.conf.base import Device

def parse(deviceName, deviceOS, cliCommand, cliResult):
    dev=Device(name=deviceName, os=deviceOS)
    dev.custom.abstraction = {"order":["os"]}
    data = dev.parse(cliCommand, output=cliResult)
    
    return data

