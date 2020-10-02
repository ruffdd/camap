from flask import Flask,render_template,send_file,send_from_directory
app = Flask(__name__,static_url_path='/static')

@app.route('/', methods=['GET'])
def root():
    return send_file('./static/index.html')

@app.route('/leaflet/<path:path>', methods=['GET'])
def leaflet(path):
    return send_from_directory('libs/leaflet',path)
