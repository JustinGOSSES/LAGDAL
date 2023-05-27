import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
from src import startWithInputOfLatLongString


app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/explore')
def explore():
   print('Request for explore page received')
   return render_template('explore.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
   
@app.route('/fieldStopIntro', methods=['POST'])
def fieldStopIntro():
    data = request.json
    if 'latitude' in data and 'longitude' in data:
        if (type(data['latitude']) == float and type(data['longitude'] == float)):
            latitude = data['latitude']
            longitude = data['longitude']
            response = {'latitude': latitude, 'longitude': longitude}
            # function that calls LLM, returns full json of response
            latLongAsString = "latitude = "+str(latitude)+", longitude = "+str(longitude)
            response = startWithInputOfLatLongString(latLongAsString)
            return jsonify(response)
        else:
            return jsonify({'error': 'Invalid input, expects floats in value of latitude and longitude keys'})
    else:
        return jsonify({'error': 'Invalid input, expects an object with keys of latitude and longitude'})

# if __name__ == '__main__':
#    app.run(host='0.0.0.0')

if __name__ == '__main__':
    app.run(debug=True)