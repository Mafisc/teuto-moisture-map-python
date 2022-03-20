# app.py
from flask import Flask, request
import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from .payload import PayloadParserFactory

# ===========
# Config 
# ===========

bucket = os.environ.get('TMM_BUCKET')
apikey = os.environ.get('TMM_API_KEY')

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
    request_apikey = request.headers.get(key="webhook-api-key", default=None)

    if(apikey is None or request_apikey == apikey):

        if request.is_json:
            message = request.get_json()
            writeJsonToDb(message)
            return message, 201
        return {"error": "Request must be JSON"}, 415
    
    else:
        return {"error" : "Unauthorized"}, 401


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

    # Extract TTN metadata from the payload
    # TODO: Move this into the PayloadParser abstract class and call from each instance
    device_id = json["end_device_ids"]["device_id"]
    device_brand = json["uplink_message"]["version_ids"]["brand_id"]
    device_model = json["uplink_message"]["version_ids"]["model_id"]
    
    received_at = json["received_at"]

    try:
        latitude = float(json["uplink_message"]["locations"]["user"]["latitude"])
    except:
        latitude = None

    try:
        longitude = float(json["uplink_message"]["locations"]["user"]["longitude"])
    except:
        longitude = None

    try:
        altitude = float(json["uplink_message"]["locations"]["user"]["altitude"])
    except:
        altitude = 0.0
    
    # Extract sensor data
    payload_parser = PayloadParserFactory.get_parser_for_model(brand=device_brand, model=device_model)
    data = payload_parser.parse_payload(json)

    app.logger.info("Got values:\n Bat:" + str(data["battery"]) + ", Conductivity: " + str(data["conductivity"]) + ", Temperature: " + str(data["temperature"]) + ", Moisture: " + str(data["moisture"]) )


    with InfluxDBClient.from_config_file(config_file="config.ini") as client:
        
        write_api = client.write_api(write_options=SYNCHRONOUS)

        bat_point = create_point_with_common_attributes("battery", \
             device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("voltage", data["battery"]) \
            .field("unit", data["battery_unit"]) \

        conductivity_point = create_point_with_common_attributes("conductivity", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("uS/cm", data["conductivity"]) \
            .field("unit", data["conductivity_unit"]) \

        temp_point = create_point_with_common_attributes("temperature", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("celsius", data["temperature"]) \
            .field("unit", data["temperature_unit"]) \

        moisture_point = create_point_with_common_attributes("moisture", \
            device_id, device_brand, device_model, longitude, latitude, altitude, received_at)\
            .field("percent", data["moisture"]) \
            .field("unit", data["moisture_unit"]) \

        write_api.write(bucket=bucket, record=bat_point)
        write_api.write(bucket=bucket, record=conductivity_point)
        write_api.write(bucket=bucket, record=temp_point)
        write_api.write(bucket=bucket, record=moisture_point)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
