from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import InputRequired
import pandas as pd
from utils import model_predict

app = Flask(__name__)
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
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if file and allowed_file(filename):
            df = model_predict(file.read().decode("utf-8")).sort_values('Predicted IC50 value (nM)')
            upload = Upload(filename=filename,data = df)
            return render_template('acetylcho.html',success_message = 'File successfully uploaded!',headings = list(df),data = df.values.tolist())
        else:
            error_message = 'Please upload a correct file (.txt)!'
            return render_template('acetylcho.html', error_message=error_message)
    return render_template('acetylcho.html',error_message='')


if __name__=='__main__':
    app.run(debug=True)