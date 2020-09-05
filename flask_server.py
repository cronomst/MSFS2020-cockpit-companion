from flask import Flask, jsonify
from SimConnect import *
from time import sleep

app = Flask(__name__)

### SIMCONNECTION RELATED STARTUPS

# create simconnection
sm = SimConnect()

# create Request
myRequest = sm.newRequest(time=2000)  # set auto data collection time @ 2s

# add required definitions output data name, definition from SDK
myRequest.add('Altitude', (b'Plane Altitude', b'feet'))
myRequest.add('Latitude', (b'Plane Latitude', b'degrees'))
myRequest.add('Longitude', (b'Plane Longitude', b'degrees'))
myRequest.add('Kohlsman', (b'Kohlsman setting hg', b'inHg'))

@app.route('/json/')
@app.route('/json/all')
def json_add_data():

    attempts = 0
    data = None

    while data is None and attempts < 20:
        sm.RequestData(myRequest)
        sm.Run()
        data = sm.GetData(myRequest)
        if data == None:
            sleep (0.5)
        attempts = attempts + 1

    if data is None:
        data_dictionary = {
            "Status": "failed to access simulator despite repeated attempts"
        }
    else:
        data_dictionary = {
            "Status": "success",
            "Altitude": data.Altitude,
            "Latitude": data.Latitude,
            "Longitude": data.Longitude,
            "Kohlsman": data.Kohlsman
        }

        return jsonify(data_dictionary)

app.run(host='0.0.0.0', port=5000, debug=True)