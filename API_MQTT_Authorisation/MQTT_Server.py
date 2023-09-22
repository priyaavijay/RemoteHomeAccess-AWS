import table as tb
import paho.mqtt.client as mqtt
import time
import json
threshold_device=120
broker_address="localhost"
broker_subscribing_url="smarthome/status"
broker_publishing_url="smarthome/command"
node_id="Server"

#MQTT_Functions_Start
def on_log(client,userdata,level,buf):
    # print("log: "+buf)
    pass

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("Connected OK")
        client.subscribe(broker_subscribing_url)
    else:
        print("Bad connection Returned code=",rc)

def on_disconnect(client,userdata,flags,rc=0):
    print("DisConnected result code"+str(rc))

def on_message(client,userdata,msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8"))
    details=m_decode
    details=details.split("/")
    router_id=details[0]
    group_id=details[1]
    device_id=details[2]
    status=details[3]
    print("router_id:",router_id,"group_id:",group_id," device_id:",device_id,"status",status)
    tb.insert_into_status(router_id,group_id,device_id,status)

def publishing_command():
    tb.set_current_time()
    tb.set_difference_time()
    tb.remove_device_status(threshold_device)
    for message in tb.table_queue():
        print(message)
        client.publish(broker_publishing_url,message,qos=2)

#MQTT_Functions_End
broker=broker_address
client=mqtt.Client(node_id,clean_session=True)
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
