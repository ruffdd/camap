from flask import Flask,render_template,send_file,send_from_directory,request,Response
from os import getenv
import traceback
import db

app = Flask(__name__,static_url_path='/static')
development= getenv("FLASK_ENV")=="development"
db.devlopment=development
if development:
    app.logger.setLevel(10)
else:
    app.logger.setLevel(30)
db.setup(app)


@app.route('/', methods=['GET'])
def root():
    return send_file('./static/index.html')

@app.route('/api/building/r<int:osm_id>',methods=['GET'])
def get_building(osm_id):
    return db.get_building(osm_id)

@app.route('/api/building',methods=['POST'])
def set_building():
    json = request.form.to_dict()
    response = Response()
    try:
        db.update_building(json)
        response.status_code = 204
    except:
        response.status_code = 406
        app.logger.debug(traceback.print_exc())
    response.headers.set('Location','/')
    return response

if development:
    @app.route('/deb/mysql/print',methods=['GET'])
    def debug():
        text=str(db.tables()).replace('(','').replace(')','').replace('[','').replace(']','').replace("'",'').replace(',',"<br>")
        return text
