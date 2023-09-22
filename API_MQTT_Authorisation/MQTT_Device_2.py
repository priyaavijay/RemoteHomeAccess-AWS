import table as tb
import paho.mqtt.client as mqtt
import datetime as dt
import time
import json
dev_device_id='LIGHT2'
dev_router_id='ABCD456'
dev_status='OFF'
current_time=0
prev_time=0
time_threshold=10
dev_device_id=str(dev_device_id).upper()
dev_router_id=str(dev_router_id).upper()
broker_address="localhost"
device_publishing_url="smarthome/status"
device_subscribing_url="smarthome/command"
node_id=dev_router_id+dev_device_id
#MQTT_Functions_Start
def on_log(client,userdata,level,buf):
    #print("log: "+buf)
    pass

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("Connected OK")
        client.subscribe(device_subscribing_url)
    else:
        print("Bad connection Returned code=",rc)

def on_disconnect(client,userdata,flags,rc=0):
    print("DisConnected result code"+str(rc))

def on_message(client,userdata,msg):
    global dev_status,dev_router_id,dev_device_id
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8"))
    details=m_decode
    details=details.split("/")
    router_id=details[0]
    device_id=details[1]
    status=details[2]
    print("router_id:",router_id," device_id:",device_id,"status",status)
    if(dev_router_id==router_id):
        if(dev_device_id==device_id):
#             print("Same ID")
#             print(status)
            if(dev_status!=status):
#                 print("Different")
                dev_status=status
                client.publish(device_publishing_url,str(dev_router_id+"/"+dev_device_id+"/"+dev_status))

def publishing_command():
    global current_time,prev_time
    if(current_time==0):
        client.publish(device_publishing_url,str(dev_router_id+"/"+dev_device_id+"/"+dev_status))
        current_time=dt.datetime.now()
        prev_time=current_time
    else:
        current_time=dt.datetime.now()
        time_taken=current_time-prev_time
        time_taken=int(time_taken.seconds)
        if(time_taken>time_threshold):
#             print(current_time,"  ",prev_time,"  ",time_taken)
            client.publish(device_publishing_url,str(dev_router_id+"/"+dev_device_id+"/"+dev_status))
            prev_time=current_time

broker=broker_address
client=mqtt.Client(node_id)
client.on_connect=on_connect
client.on_log=on_log
client.on_disconnect=on_disconnect
client.on_message=on_message
print("Connecting to broker",broker)
client.connect(broker)
while(1):
    client.loop()
    publishing_command()
client.disconnect()
