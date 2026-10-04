from fastapi import FastAPI, Path, HTTPException
import json
app = FastAPI()

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data
     
@app.get("/")
def name():
    return {'message': 'Patient Management System API'}

@app.get("/about")
def about():
    return {'message':'Fully Fuctional Patient Management System API'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def specific_patient(patient_id :str = Path(..., description= "ID of the Patient in DB", example = 'P001')):
    data = load_data()
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(
        status_code = 404,
        detail= "Not Found"
    )
