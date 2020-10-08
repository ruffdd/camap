from flask import Flask,render_template,send_file,send_from_directory
from os import getenv
import db
app = Flask(__name__,static_url_path='/static')
development= getenv("FLASK_ENV")=="development"
if development:
    app.logger.setLevel(10)
else:
    app.logger.setLevel(30)
db.setup(app)


@app.route('/', methods=['GET'])
def root():
    return send_file('./static/index.html')

@app.route('/leaflet/<path:path>', methods=['GET'])
def leaflet(path):
    return send_from_directory('libs/leaflet',path)

@app.route('/api/building/r<int:osm_id>',methods=['GET'])
def get_building(osm_id):
    return db.get_building(osm_id)

if development:
    @app.route('/deb/mysql/print',methods=['GET'])
    def debug():
        text=str(db.tables()).replace('(','').replace(')','').replace('[','').replace(']','').replace("'",'').replace(',',"<br>")
        return text
