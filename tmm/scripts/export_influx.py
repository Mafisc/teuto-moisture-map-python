from influxdb_client import InfluxDBClient
import sys

def export_to_json(path_to_config="../config.ini", query_type='value'):

    value_query = 'from(bucket: "tmm-bucket") \
    |> range(start: v.timeRangeStart, stop:v.timeRangeStop) \
    |> filter(fn: (r) => \
        r._measurement == "moisture" and \
        r._field == "percent"'

    map_query = 'lat = from(bucket: "tmm-bucket") \
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
    |> filter(fn: (r) => r["_measurement"] == "moisture") \
    |> filter(fn: (r) => r["_field"] == "latitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    \
    long = from(bucket: "tmm-bucket") \
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
    |> filter(fn: (r) => r["_measurement"] == "moisture") \
    |> filter(fn: (r) => r["_field"] == "longitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    \
    moisture = from(bucket: "tmm-bucket") \
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
    |> filter(fn: (r) => r["_measurement"] == "moisture") \
    |> filter(fn: (r) => r["_field"] == "percent") \
    |> aggregateWindow(every: 1d , fn: last) \
    \
    alt = from(bucket: "tmm-bucket") \
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
    |> filter(fn: (r) => r["_measurement"] == "moisture") \
    |> filter(fn: (r) => r["_field"] == "altitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    \
    union(tables: [alt, lat, long, moisture]) \
    |> group(columns: ["device"], mode: "by") \
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value") \
    |> group()'

    query = value_query

    if query_type == 'map':
        query = map_query

    with InfluxDBClient.from_config_file(config_file=path_to_config) as client:

        query_api = client.query_api()
        result = query_api.query(query=query)
        print(result)

args = sys.argv[1:]
path = args[0]
type = args[1]

export_to_json(path_to_config=path, query_type=type)