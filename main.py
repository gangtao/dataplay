from flask import Flask, request, make_response, redirect, url_for, jsonify
from flask.ext.script import Manager

import csv
import os
import os.path
import glob
import json

from rviz import Builder
from rviz import SampleData

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__,static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#manager = Manager(app)

@app.route('/') 
def index():
    return app.send_static_file('index.html')

@app.route('/csvdata', methods=['GET', 'POST']) 
def listcsvdata():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename ; ## Security issue
            ## TODO, check duplicated file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
        return 'Post Data not supported!'
    else:
        flist = [ f.replace('./data/','').replace('.csv','') for f in glob.glob('./data/*.csv')]
        return json.dumps(flist)

@app.route('/data/<dataname>') 
def getdata(dataname):
    fpath = './data/' + dataname + '.csv'
    if not os.path.isfile(fpath):
        return make_response('<h1>File %s does not exist!</h1>' % fpath) 
    
    with open(fpath, 'rb') as csvfile:
        return jsonify(name=dataname, csv=csvfile.read())

@app.route('/rdata') 
def listrdata():
    return json.dumps(SampleData().getlist())

@app.route('/rdata/<dataname>') 
def getrdata(dataname):
    csvstr = SampleData().getdata(dataname)
    if csvstr is not None:
        return jsonify(name=dataname, csv=csvstr)
    else:
        return "Bad Request", 400


@app.route('/viz', methods=['POST'])
def visualize():
    print request.form
    vizbuilder = Builder(request.form)
    result = vizbuilder.build()
    return jsonify(src=result)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.debug = True
    #manager.run(app)
    app.run()