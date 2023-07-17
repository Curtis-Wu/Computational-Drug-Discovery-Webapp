from flask import Flask,render_template,request,send_file,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import InputRequired
import pandas as pd
from utils import model_predict
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()

@app.route('/')
def index():
    return render_template('index.html')

class Upload(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.String)

def allowed_file(filename):
    if len(filename)<=3:
        return False
    return True if filename[-3:]=='txt' else False

@app.route('/acetylcholinesterase/',methods = ['GET','POST'])
def acetylcho():    
    return render_template('acetylcho.html')

@app.route('/download/<variable>/')
def download_file(variable):
    file = 'models/acetylcholinesterase/data/user_data_'+str(variable)+'.csv'
    return send_file(file,as_attachment=True)

@app.route('/upload/',methods = ['POST'])
def upload_file():
    data = request.json
    filecontent = data.get('fileContent')
    filename = data.get('filename')
    df = model_predict(filecontent).sort_values('Predicted IC50 value (nM)')
    upload = Upload(filename=filename,data = filecontent)
    db.session.add(upload)
    db.session.commit()
    df.to_csv('models/acetylcholinesterase/data/user_data_'+str(upload.id)+'.csv',index=False)
    session['headings'] = list(df)
    session['data'] = df.values.tolist()
    session['id'] = str(upload.id)
    return 'File successfully uploaded'

@app.route('/compounds/')
def compounds():
    return render_template('compounds.html')


@app.route('/results/')
def results():
    headings = session.get('headings', [])
    data = session.get('data', [])
    id = session.get('id',[])
    
    # Clear the session variables
    session.pop('headings', None)
    session.pop('data', None)
    session.pop('id',None)

    if id: file_download = "Download csv file here"
    return render_template('results.html', headings=headings, data=data, id=id, file_download = file_download)


@app.route('/method/')
def methods():
    return render_template('method.html')

@app.route('/references/')
def references():
    return render_template('references.html')


if __name__=='__main__':
    app.run(debug=True)