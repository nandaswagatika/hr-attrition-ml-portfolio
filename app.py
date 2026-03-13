from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("hr_attrition_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = {
        'Age': data.get('Age', 30),
        'OverTime': data.get('OverTime', 'No'),
        'Department': data.get('Department', 'Sales'),
        'MonthlyIncome': data.get('MonthlyIncome', 6500),
        'DistanceFromHome': 2, 'PercentSalaryHike': 12, 'TotalWorkingYears': 7,
        'YearsAtCompany': 4, 'YearsInCurrentRole': 2, 'YearsSinceLastPromotion': 1,
        'YearsWithCurrManager': 3, 'TrainingTimesLastYear': 2, 'JobInvolvement': 3,
        'JobSatisfaction': 3, 'EnvironmentSatisfaction': 3, 'WorkLifeBalance': 3,
        'JobLevel': 2, 'StockOptionLevel': 0, 'BusinessTravel': 'Travel_Rarely',
        'EducationField': 'Life Sciences', 'Gender': 'Male', 'JobRole': 'Laboratory Technician',
        'MaritalStatus': 'Married', 'Education': 3, 'RelationshipSatisfaction': 3
    }
    
    df = pd.DataFrame([input_data])
    risk = model.predict_proba(df)[0][1]
    
    return jsonify({
        "risk": round(risk, 3),
        "level": "HIGH RISK" if risk > 0.5 else "LOW RISK",
        "action": "CALL NOW" if risk > 0.5 else "MONITOR"
    })

@app.route('/')
def home():
    return "HR Attrition API LIVE - POST to /predict"

if __name__ == '__main__':
    app.run(debug=True)
