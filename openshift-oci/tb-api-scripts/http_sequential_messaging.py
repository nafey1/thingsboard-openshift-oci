import csv
import logging
import configparser
from time import time
import requests
from tb_rest_client.rest import ApiException
from tb_rest_client.rest_client_ce import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    config = readConfig()
    csv_has_header = config['Config'].getboolean('csv_has_header')
    rows_per_message = config['Config'].getint('rows_per_message')
    time_offset = config['Config'].getint('time_offset')
    time_step = config['Config'].getint('time_step')
    row_count = config['Config'].getint('row_count')
    filename = config['Config']['csv_file']
    device_route = config['Config']['device_http_route']

    try: 
        currentTimeMs = round(time() * 1000)
        startTime = currentTimeMs - (time_step * row_count) #get current time in ms minus an offset
        messages = []

        with open(filename, 'r') as file:
            skippedHeader:bool = False
            reader = csv.reader(file)
            idx = 0
            for row in reader:
                print(f'row: {idx}')
                if not skippedHeader and csv_has_header:
                    skippedHeader = True
                    continue
                idx = idx + 1
                rowlist:list[float] = list(map(float,row)) #Get the csv row as a list of floats
                messageTime = (startTime + (idx * time_step))
                messageData = {
                    "ts": messageTime,
                    "values": {"data": rowlist}
                }
                messages.append(messageData)
                var = idx
                if var % rows_per_message == 0:
                    sendHTTP(device_route, messages)
                    messages = []
            if idx % rows_per_message != 0:
                sendHTTP(device_route, messages)
        exit()
    except Exception as e:
        print(f"Exception: {e}")

#parse config and return config object
def readConfig():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

def sendHTTP(url, data):
    response = requests.post(url, str(data))

if __name__ == '__main__':
    main()

#mosquitto_pub -d -q 1 -h tb-route-node-root-thingsboard.apps.ociopenshift.test-app.cloud -p 1883 -t v1/devices/me/telemetry -u "63okHXnboSMhRw596aPF" -m "{temperature:25}"
#mosquitto_pub -d -q 1 -h demo.thingsboard.io -p 1883 -t v1/devices/me/telemetry -u "t3D3PodiW2obWAYypFZQ" -m "{temperature:25}"
#-d : debug
#-q : qos (Quality of service = 1)
#-h : host <url>
#-p : port <port>
#-t : topic <topic>
#-u : username <username> (token)
#-m : message <message> 
