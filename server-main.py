from flask import Flask,render_template,send_file
app = Flask(__name__,static_url_path='/static')

@app.route('/', methods=['GET'])
def root():
    return send_file('./static/index.html')

