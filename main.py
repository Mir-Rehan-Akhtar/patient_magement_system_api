from fastapi import FastAPI
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

