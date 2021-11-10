# Teuto Moisture Map (Python)

This project contains a small python app that acts as the receiving end for a webhook in TheThingsNetwork. The purpose of this app is to collect environmental data from a number of sensors and store the sensor's readings in a database.

***
**! In its current state the app is but a prototype !**
***

## Supported sensors
As of now the app has only been tested with the Dragino Moisture Sensor (<http://www.dragino.com/>). Exrtracting the readings from the payload might not work if a different sensor is used.

## Prerequisites
1. The sensor must be registered in TTN (<https://www.thethingsnetwork.org/>).
2. An Application must be created in TTN and the sensor needs to be assigned to it.
3. Within the Application, a webhook must be created that points to the correct hostname, port and path.
4. As of now the app only works with InfluxDB (<https://www.influxdata.com/>). You either need an InfluxDB 2.0 Cloud account or some other host running InfluxDB 2.0.
5. Put your InfluxDB 2.0 connection configuration into a file called **config.ini** (see: <https://influxdb-client.readthedocs.io/en/latest/api.html#influxdb_client.InfluxDBClient.from_config_file>)

If everything has been set up correctly, you should see measurements piling into your selected InfluxDB bucket :-)

## Running the app

To run the app without docker: 

    python app.py

Building the docker image:

    docker build . -t your/tag
    docker run -p 0.0.0.0:5000:5000 your/tag

Make sure that port 5000 is reachable from the outside world.
