from flask import Flask,render_template,request,send_file,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from utils import model_predict
import pandas as pd
import os,io
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()

class mol_acetylcho(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.String)

class mol_vegfr2(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.String)

class mol_bace1(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.String)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/method/')
def methods():
    return render_template('method.html')

@app.route('/references/')
def references():
    return render_template('references.html')

@app.route('/acetylcholinesterase/')
def acetylcho():    
    return render_template('acetylcho.html')

@app.route('/vegfr2/')
def vegfr2():    
    return render_template('vegfr2.html')

@app.route('/bace1/')
def bace1():
    return render_template('bace1.html')

@app.route('/compounds/')
def compounds():
    return render_template('compounds.html')


@app.route('/upload/',methods = ['POST'])
def upload_file():

    data = request.json
    filecontent = data.get('fileContent')
    filename = data.get('filename')
    compound_name = data.get('compound_name')
    
    df = model_predict(compound_name,filecontent).sort_values('Predicted IC50 value (nM)')
    df['Predicted IC50 value (nM)'] = df['Predicted IC50 value (nM)'].astype('float64').round(3)

    if compound_name == "acetylcholinesterase":
        upload = mol_acetylcho(filename=filename,data = filecontent)
        db.session.add(upload)
        db.session.commit()
        df.to_csv('models/acetylcholinesterase/data/'+str(upload.id)+'.csv',index=False)

    elif compound_name == "vegfr2":
        upload = mol_vegfr2(filename=filename,data = filecontent)
        db.session.add(upload)
        db.session.commit()
        df.to_csv('models/vegfr2/data/'+str(upload.id)+'.csv',index=False)

    elif compound_name == "bace1":
        upload = mol_bace1(filename=filename,data = filecontent)
        db.session.add(upload)
        db.session.commit()
        df.to_csv('models/bace1/data/'+str(upload.id)+'.csv',index=False)

    session['headings'] = list(df)
    session['data'] = df.values.tolist()
    session['id'] = str(upload.id)
    session['name'] = compound_name

    return "file successfully uploaded"


@app.route('/results/')
def results():
    headings = session.get('headings', [])
    data = session.get('data', [])
    id = session.get('id',[])
    name = session.get('name',[])
    
    # Clear the session variables
    session.pop('headings', None)
    session.pop('data', None)
    session.pop('id',None)

    if name=="acetylcholinesterase": 
        name = "Acetylcholinesterase"
    
    elif name == "vegfr2":
        name = "VEGF Receptor-2"

    elif name == "bace1":
        name = "Beta-Secretase 1"

    return render_template('results.html', name=name,headings=headings, data=data, id=id, file_download = "Download csv file here")


@app.route('/download/<variable>/')
def download_file(variable):
    name = session.get('name',[])
    session.pop('name',None)

    file_path = 'models/'+name+'/data/'+str(variable)+'.csv'
    
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(file_path)
        
    return send_file(return_data, mimetype='csv', as_attachment=True,download_name = file_path)


if __name__=='__main__':
    app.run(debug=True)