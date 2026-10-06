from fastapi import FastAPI, Path, HTTPException, Query
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
@app.get('/sort')
def sort_patient(sorted_by: str = Query(...,description="The Patient record can be sorted by age, hight,bmi"),
                  order : str = Query('asc', description="sort in ascendig or descending order.") ):
    valid_fields = ['age','height','bmi']
    if sorted_by not in valid_fields:
        raise HTTPException(
            status_code= 400,
            detail= f"Invalid Field selected form {valid_fields}"
        )
    if order not in ['asc','desc']:
        raise HTTPException(
            status_code=400,
            detail='Invalid order selected '
        )
    data = load_data()
    sorted_order = True if order=='desc' else False
    sorted_data = sorted(data.values(),key = lambda x : x.get(sorted_by,0),reverse=sorted_order)
    return sorted_data
