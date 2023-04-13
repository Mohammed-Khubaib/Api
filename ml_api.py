from flask import Flask,request,jsonify
import pickle
import numpy as np
import pandas as pd

model = pickle.load(open('pipe7.pkl','rb'))

def Balls(ball_No,n):
  return (ball_No)*10 - 4*n
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world"

@app.route('/predict',methods=['POST'])
def predict():
    target = int(request.form.get('target'))
    score = int(request.form.get('score'))
    over = int(request.form.get('over'))
    wicket = int(request.form.get('wicket'))
    # over number rounding :
    # it is to convert the over number into Balls
    r = round(over)
    Overs=Balls(over,r)
    runs_left=target-score
    balls_left=round(120-Overs)
    wicket=10-wicket
    crr=score/over
    rrr=(runs_left*6)/balls_left
    input_df=pd.DataFrame({
        'runs_left':[runs_left], 
        'balls_left':[balls_left],
        'wickets':[wicket], 
        'total_runs_x':[target],
        'crr':[crr],
        'rrr':[rrr]
        })
    result= model.predict_proba(input_df)
    loss=result[0][0]
    win=result[0][1]
    return jsonify({'loss':str(loss*100),'win':str(win*100)})

if __name__ == '__main__':
    app.run()