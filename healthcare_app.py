import pickle
import numpy as np
import os
from flask import Flask, render_template,request, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
from flask_cors import  cross_origin

app = Flask(__name__)

model_heartdisease = pickle.load(open('heartdisease.pkl', 'rb'))
model_liverdisease = pickle.load(open('liverdisease.pkl', 'rb'))
model_cancer = pickle.load(open('breastcancer.pkl', 'rb'))
model_malaria = load_model('malariadisease.h5')
model_pneumonia = load_model('pneumonia_disease.h5')

@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/appointmentform',methods=['GET'])
def appointmentform():
    return render_template('appointmentform.html')

@app.route('/contact',methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/firstaid',methods=['GET'])
def firstaid():
    return render_template('firstaid.html')

@app.route('/service',methods=['GET'])
def service():
    return render_template('service.html')

@app.route('/heartdisease', methods=['GET','POST'])
def heartdisease():
    if request.method == 'POST':
        Age=int(request.form['age'])
        Gender=int(request.form['sex'])
        ChestPain= int(request.form['cp'])
        BloodPressure= int(request.form['trestbps'])
        ElectrocardiographicResults= int(request.form['restecg'])
        MaxHeartRate= int(request.form['thalach'])
        ExerciseInducedAngina= int(request.form['exang'])
        STdepression= float(request.form['oldpeak'])
        ExercisePeakSlope= int(request.form['slope'])
        MajorVesselsNo= int(request.form['ca'])
        Thalassemia=int(request.form['thal'])
        prediction=model_heartdisease.predict([[Age, Gender, ChestPain, BloodPressure, ElectrocardiographicResults, MaxHeartRate, ExerciseInducedAngina, STdepression, ExercisePeakSlope, MajorVesselsNo, Thalassemia]])
        if prediction==1:
            return render_template('prediction.html', greet="Oops!", prediction="You have Heart Disease.")
        else:
            return render_template('prediction.html', greet="Congrats!", prediction="You are Normal.")
    else:
        return render_template('heartdisease.html')

    
@app.route('/liverdisease', methods=['GET','POST'])
def liverdisease():
    if request.method == 'POST':
        Age=int(request.form['Age'])
        Gender=int(request.form['Gender'])
        Total_Bilirubin= float(request.form['Total_Bilirubin'])
        Direct_Bilirubin= float(request.form['Direct_Bilirubin'])
        Alkaline_Phosphotase= int(request.form['Alkaline_Phosphotase'])
        Alamine_Aminotransferase= int(request.form['Alamine_Aminotransferase'])
        Aspartate_Aminotransferase= int(request.form['Aspartate_Aminotransferase'])
        Total_Protiens= float(request.form['Total_Protiens'])
        Albumin= float(request.form['Albumin'])
        Albumin_and_Globulin_Ratio= float(request.form['Albumin_and_Globulin_Ratio'])
        prediction=model_liverdisease.predict([[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio]])
        if prediction==1:
            return render_template('prediction.html', greet="Oops!", prediction="You have Liver Disease.")
        else:
            return render_template('prediction.html', greet="Congrats!", prediction="You are Normal.")
    else:
        return render_template('liverdisease.html')

@app.route('/breastcancer', methods=['GET','POST'])
def breastcancer():
    if request.method == 'POST':
        texture_mean = float(request.form['texture_mean'])
        perimeter_mean = float(request.form['perimeter_mean'])
        smoothness_mean = float(request.form['smoothness_mean'])
        compactness_mean = float(request.form['compactness_mean'])
        concavity_mean = float(request.form['concavity_mean'])
        concave_points_mean = float(request.form['concave_points_mean'])
        symmetry_mean = float(request.form['symmetry_mean'])
        radius_se = float(request.form['radius_se'])
        compactness_se = float(request.form['compactness_se'])
        concavity_se = float(request.form['concavity_se'])
        concave_points_se = float(request.form['concave_points_se'])
        texture_worst = float(request.form['texture_worst'])
        smoothness_worst = float(request.form['smoothness_worst'])
        compactness_worst = float(request.form['compactness_worst'])
        concavity_worst = float(request.form['concavity_worst'])
        concave_points_worst = float(request.form['concave_points_worst'])
        symmetry_worst = float(request.form['symmetry_worst'])
        fractal_dimension_worst = float(request.form['fractal_dimension_worst'])
        prediction=model_cancer.predict([[texture_mean, perimeter_mean, smoothness_mean, compactness_mean,
           concavity_mean, concave_points_mean, symmetry_mean, radius_se,
           compactness_se, concavity_se, concave_points_se, texture_worst,
           smoothness_worst, compactness_worst, concavity_worst,
           concave_points_worst, symmetry_worst, fractal_dimension_worst]])
        if prediction==1:
            return render_template('prediction.html', greet="Oops!", prediction="The tumor is malignant.")
        else:
            return render_template('prediction.html', greet="Great!", prediction="The tumor is benign.")
    else:
        return render_template('breastcancer.html')

# Image Preprocessing
def malaria_predict(img_path):
    img = image.load_img(img_path, target_size=(30, 30, 3))
    x=image.img_to_array(img)
    x=x/255
    x=np.expand_dims(x, axis=0)
    preds = model_malaria.predict(x)
    return preds

def pneumonia_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    
    x=image.img_to_array(img)
    x=x/255
    x=np.expand_dims(x, axis=0)
    preds = model_pneumonia.predict(x)
    return preds

@app.route('/malariadisease', methods=['GET', 'POST'])
def malariadisease():
    if request.method=="GET":
        return render_template('malariadisease.html')
    else:
        f=request.files["file"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'uploads',  secure_filename(f.filename))
        f.save(file_path)

        prediction = malaria_predict(file_path)
        if prediction[0][0]>=0.5:
            return render_template('prediction.html', greet="Oops!", prediction="You have Malaria.")
        else:
            return render_template('prediction.html', greet="Wow!", prediction="You have Normal.")

@app.route('/pneumoniadisease', methods=['GET', 'POST'])
def pneumoniadisease():
    if request.method=="GET":
        return render_template('pneumoniadisease.html')
    else:
        f=request.files["file"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'uploads',  secure_filename(f.filename))
        f.save(file_path)

        prediction = pneumonia_predict(file_path)
        pred=np.argmax(prediction, axis=1)
        if pred[0]==1:
            return render_template('prediction.html', greet="Oops!", prediction="You have Pneumonia.")
        else:
            return render_template('prediction.html', greet="Great!", prediction="You are Normal.")

@cross_origin()
@app.route('/diabetes',methods=['GET','POST'])
def diabetes():
    if request.method == "POST":
        Pregnancies = float(request.form['Pregnancies'])
        Glucose = float(request.form['Glucose'])
        BloodPressure = float(request.form['BloodPressure'])
        SkinThickness = float(request.form['SkinThickness'])
        Insulin = float(request.form['Insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
        Age = float(request.form['Age'])

        filename = 'modelForPrediction.sav'
        loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
        scalar = pickle.load(open("sandardScalar.sav", 'rb'))
        # predictions using the loaded model file
        prediction = loaded_model.predict(scalar.transform(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]))
        if prediction ==[1]:
                prediction = "You have Diabetes"
                greet = "Oops!"

        else:
                prediction = "You are Normal"
                greet = "Congrats!"
        return render_template('prediction.html', greet=greet, prediction=prediction)
    return render_template('diabetes.html')

@app.route('/corona', methods=["GET", "POST"])
def corona():
    file = open('corona.pkl', 'rb')
    clf = pickle.load(file)
    file.close()
    if request.method == "POST":
        myDict = request.form
        fever = int(myDict['fever'])
        age = int(myDict['age'])
        pain = int(myDict['pain'])
        runnyNose = int(myDict['runnyNose'])
        diffBreath = int(myDict['diffBreath'])
        # Code for Inference
        inputFeatures = [fever, pain, age, runnyNose, diffBreath]
        infProb = clf.predict_proba([inputFeatures])[0][1]
        if round(infProb * 100) >= 50:
            prediction = "You may have COVID"
            greet = "Oops!"
        else:
            prediction = "You are Normal"
            greet = "Great!"
        return render_template('prediction.html', greet=greet, prediction=prediction)
    return render_template('corona.html')

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory('uploads', filename)

if __name__=='__main__':
	app.run(debug=True)

