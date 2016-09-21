from network_test import * # for ping
import sys # for OS calls

from datetime import datetime # for getting current time and date

import subprocess

from scapy.all import srp, Ether, ARP # used for arp-scan

import paho.mqtt.client as mqtt


TIMEOUT = 1000 
N_SAMPLE = int(sys.argv[1]) 
hwid = sys.argv[2]
IP =  sys.argv[3]

MQTT_SERVER = sys.argv[4]
MQTT_USERNAME = sys.argv[5]
MQTT_PASSWD = sys.argv[6]



mqtt_client = mqtt.Client(client_id = hwid, clean_session = True)
mqtt_client.username_pw_set(MQTT_USERNAME, password = MQTT_PASSWD)
mqtt_client.connect(MQTT_SERVER, 1883, 60)

TEMP_TOPIC = 'v1/' + hwid + '/sensor/temperature'
HUMI_TOPIC = 'v1/' + hwid + '/sensor/humidity'
SELF_TOPIC = 'v1/' + hwid + '/status/self'
ERROR_TOPIC = 'v1/' + hwid + '/status/error'


SCAN_IP_RANGE = '150.162.10.0/24'

PATH_TO_LOG = 'log_lat_peak.txt'

def store_data(data, file_path, mode):
    with open(file_path, mode) as file:
        file.write(data)

def arp_scan():
    alive,dead=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=SCAN_IP_RANGE), timeout=2, iface='eno1' ,verbose=0)

    client_list = ''

    for i in range(0,len(alive)):
            info = alive[i][1].hwsrc + " - " + alive[i][1].psrc
            client_list += info + '\n'

    return client_list

def mqtt_publish(topic, data):
    mqtt_client.publish(topic, data)

network = NetworkLatencyBenchmark(IP,TIMEOUT)
network.print_status = False

# Run tests for 50 samples
network.run_test(N_SAMPLE)
network.get_results()

lat = network.get_latency()
timeout = network.get_timeout_percentile()

log_time = str(datetime.now()) + '\n'

# if lat > 10:
#     print 'Saving log time'
#     store_data(log_time, PATH_TO_LOG, 'a')

#     print 'Starting arp-scan'
#     wifi_clients = arp_scan()
#     store_data(wifi_clients, log_time + '.txt', 'w')
#     mqtt_publish(ERROR_TOPIC, 1)


mqtt_publish(TEMP_TOPIC, lat)
# mqtt_publish(HUMI_TOPIC, timeout)
mqtt_publish(SELF_TOPIC, 1)










