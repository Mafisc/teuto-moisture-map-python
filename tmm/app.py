# app.py
from flask import Flask, request
import os

import re

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ===========
# Config 
# ===========

bucket = os.environ.get('TMM_BUCKET')
apikey = os.environ.get('TMM_API_KEY')

# TODO: Add mqtt client as an alternative way to get data from ttn
ttn_mqtt_topics = list()


# =====================
# Webhook web interface
# =====================

# Json WS endpoint accepting messages from TTN
app = Flask(__name__)

""" 
This method accepts JSON payloads from TTN, unmarshals the required information and persists them 
"""
@app.post("/incomingMessages")
def add_message():
    request_apikey = request.headers.get(key="X-Downlink-Apikey", default=None)

    if(apikey != None & request_apikey == apikey):

        if request.is_json:
            message = request.get_json()
            writeJsonToDb(message)
            return message, 201
        return {"error": "Request must be JSON"}, 415
    
    else:
        return {"error" : "Unauthorized"}, 401


# ===================
# Helpers
# ===================

""" 
Extracts numerical values from strings
"""
def extract_numbers_from_string(string :str) -> float:
    return re.findall("^\d+[.]*\d*", string)

"""
Extracts the unit of measurements from strings 
"""
def extract_chars_from_string(string: str) -> str: 
        return re.findall("[\w]*[°/%]*\w*$", string)


# ===========
# Persistence
# ===========

"""
Sets common attributes from a sensor to a newly created Point 
"""
def create_point_with_common_attributes(name, device_id, device_brand, device_model, longitude, latitude, altitude, received_at):
    return Point(name) \
            .tag("device", device_id) \
            .tag("device_brand", device_brand) \
            .tag("device_model", device_model) \
            .field("latitude", latitude) \
            .field("longitude", longitude) \
            .field("altitude", altitude) \
            .time(received_at)
        

""" 
Handle the actual writing of json to one or more persistence instances
"""
def writeJsonToDb(json : dict):

    app.logger.info("Received: %s", str(json))

    # Extracting the values from the message is specific to the sensor used
    # This implementation supports only the dragoni sensor as of now
    bat_value = json["uplink_message"]["decoded_payload"]["bytes"]["Bat"]
    conductivity_value = json["uplink_message"]["decoded_payload"]["bytes"]["conduct_SOIL"]
    temp_value = json["uplink_message"]["decoded_payload"]["bytes"]["temp_SOIL"]
    moisture_value = json["uplink_message"]["decoded_payload"]["bytes"]["water_SOIL"]
    device_id = json["end_device_ids"]["device_id"]
    device_brand = json["uplink_message"]["version_ids"]["brand_id"]
    device_model = json["uplink_message"]["version_ids"]["model_id"]
    # TODO: Check device_brand and device_model to support additional sensors
    
    try:
        latitude = float(json["uplink_message"]["locations"]["user"]["latitude"])
    except:
        latitude = 0.0

    try:
        longitude = float(json["uplink_message"]["locations"]["user"]["longitude"])
    except:
        longitude = 0.0

    try:
        altitude = float(json["uplink_message"]["locations"]["user"]["altitude"])
    except:
        altitude = 0.0

    battery  = float(extract_numbers_from_string(bat_value)[0])
    conductivity = float(extract_numbers_from_string(conductivity_value)[0])
    temperature = float(extract_numbers_from_string(temp_value)[0])
    moisture = float(extract_numbers_from_string(moisture_value)[0])

    battery_unit = str(extract_chars_from_string(bat_value)[0])
    conductivity_unit = str(extract_chars_from_string(conductivity_value)[0])
    temperature_unit = str(extract_chars_from_string(temp_value)[0])
    moisture_unit = str(extract_chars_from_string(moisture_value)[0])
    
    received_at = json["received_at"]

    app.logger.info("Got values:\n Bat:" + str(bat_value) + ", Conductivity: " + str(conductivity_value) + ", Temperature: " + str(temp_value) + ", Moisture: " + str(moisture_value) )

    with InfluxDBClient.from_config_file(config_file="config.ini") as client:
        
        write_api = client.write_api(write_options=SYNCHRONOUS)

        bat_point = create_point_with_common_attributes("battery", \
             device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("voltage", battery) \
            .field("unit", battery_unit) \

        conductivity_point = create_point_with_common_attributes("conductivity", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("uS/cm", conductivity) \
            .field("unit", conductivity_unit) \

        temp_point = create_point_with_common_attributes("temperature", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("celsius", temperature) \
            .field("unit", temperature_unit) \

        moisture_point = create_point_with_common_attributes("moisture", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("percent", moisture) \
            .field("unit", moisture_unit) \

        write_api.write(bucket=bucket, record=bat_point)
        write_api.write(bucket=bucket, record=conductivity_point)
        write_api.write(bucket=bucket, record=temp_point)
        write_api.write(bucket=bucket, record=moisture_point)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')