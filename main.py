from flask import Flask,render_template,request,redirect,session
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
import mysql.connector



app=Flask(__name__,template_folder='template',static_folder='static')
app.secret_key = os.urandom(24)
print("Connecting to sql.....")

conn=mysql.connector.connect(host="localhost",user="partha",password="partha@2025",database="flaskdb")
cursor=conn.cursor()
  



gd_clf_model=pickle.load(open('GradientBoostModelClassificationnew.pkl','rb'))
print("loaded...")
reg_model=pickle.load(open('GradientBoostModelnew.pkl','rb'))
label_encoder=LabelEncoder()
meal_plan_mapping={
    0:"Balanced Diet",
    1:"High-Protein Diet",
    2:"Low-Carb Diet",
    3:"Low-Fat Diet"
}

cols = [
    'Age', 'Height_cm', 'Weight_kg', 'BMI',
    'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic',
    'Cholesterol_Level', 'Blood_Sugar_Level',
    'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours',
    'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake',
    'Gender', 'Chronic_Disease', 'Genetic_Risk_Factor', 'Allergies',
    'Alcohol_Consumption', 'Smoking_Habit', 'Dietary_Habits',
    'Preferred_Cuisine', 'Food_Aversions'
]

#'Balanced Diet', 'High-Protein Diet', 'Low-Carb Diet',
       #'Low-Fat Diet'

diet_details = {
    "High Protein Diet": [
        "Chicken Breast",
        "Egg Whites",
        "Greek Yogurt",
        "Lentils",
        "Chickpeas",
        "Paneer",
        "Tofu",
        "Fish (Salmon, Tuna)",
        "Soybeans",
        "Milk"
    ],
    "Low Carb Diet": [
        "Eggs",
        "Broccoli",
        "Avocado",
        "Chicken",
        "Leafy Greens",
        "Zucchini",
        "Cheese",
        "Nuts & Seeds",
    ],
    "Balanced Diet": [
        "Whole Grains",
        "Lean Proteins",
        "Vegetables",
        "Fruits",
        "Healthy Fats",
        "Dairy",
    ],
    "Low-Fat Diet": [
        "Oats",
        "Brown Rice",
        "Green Vegetables",
        "Legumes",
        "Apple",
        "Pear",
        "Lean Proteins",
        "Olive Oil",
    ],
    
}



@app.route('/')

def wlcm():
    return render_template('welcome.html')




@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/register')
def reg():
    return render_template('register.html')




@app.route('/login_validation',methods=['GET','POST'])
def login_validation():
    email= request.form.get('email')
    password=request.form.get('password')

    cursor.execute(""" SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/welcome')
    else:
        return redirect('/')
    

@app.route('/add_user',methods=['POST'])
def home():
    name=request.form.get('uname')
    email = request.form.get('uemail')
    # phn=request.form.get('uphone')
    password = request.form.get('upassword')


    # cursor.execute(""" INSERT INTO `users` (`user_id` , `name` , `email` , `password` ) VALUES 
    #                 (NULL,'{}','{}','{}')""".format(name,email,password))
    # cursor.execute(""" INSERT INTO `users` (  `name` , `email` , `password` ) VALUES 
    #                 (%s,%s,%s)""".format(name,email,password))
    

    # new one 
    sql="INSERT INTO `users`(`name`,`email`,`password`) VALUES(%s,%s,%s)"
    values=(name,email,password)
    cursor.execute(sql,values)
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` = %s""",(email,))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/welcome')
    # return render_template('register.html')







@app.route('/welcome',methods=['GET','POST'])
def welcome():
    if 'user_id' in session:
        return render_template('welcomen.html')
    else:
        return redirect('/')
    # return render_template('welcomen.html')




   
@app.route('/predict', methods=['POST','GET'])
def predict():
    if not 'user_id' in session:
        return redirect('/login')
    try:
        features = [x for x in request.form.values()]
        print("Received values:", len(features))
        print("Expected columns:", len(cols))

        # Convert to DataFrame
        input_df = pd.DataFrame([features], columns=cols)
        print(input_df)

        # Make predictions
        meal_pred_enc = gd_clf_model.predict(input_df)[0]
        meal_pred=meal_plan_mapping.get(meal_pred_enc,"Unknown meal plan")
        nutrients_pred = reg_model.predict(input_df)[0]
        calories, protein, carbs, fats = nutrients_pred

        print("Meal Plan Prediction:", meal_pred)
        print("Nutrient Values:", calories, protein, carbs, fats)
        
        # Render result page
        return render_template(
            'result.html',
            prediction=meal_pred,
            calories=f"Calories: {calories:.2f}",
            protein=f"Protein: {protein:.2f}",
            carbs=f"Carbs: {carbs:.2f}",
            fats=f"Fats: {fats:.2f}"
        )
    

    except Exception as e:
        print("Error during prediction:", e)
        return render_template('home.html', prediction_text=f"Error: {e}")
    
    


@app.route('/details')
def details():
    if not 'user_id' in session:
        return redirect('/login')

    diet_type = request.args.get("diet")

    if diet_type not in diet_details:
        return "No details found for this diet type."

    return render_template(
        "details.html",
        diet=diet_type,
        items=diet_details[diet_type]
    )

    





@app.route('/about')
def about():

    if 'user_id' in session:
        return render_template('about.html')
    else:
        return redirect('/')
    return render_template('/about.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

print("flask app is starting....")

if __name__=="__main__":
    app.run(debug=True)







