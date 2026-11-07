from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel,Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
import json
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Enter The ID of the Patient", examples=["P001"] )]
    name : Annotated[str, Field(..., description="Name Of the Patient ")]
    city: Annotated[str, Field(..., description="The city where Patient is living ")]
    age: Annotated[int, Field(..., description= "Age of the Patient", gt=0, lt=120)]
    gender: Annotated[Literal['male','female','others'], Field(..., description="Gender of the Patient")]
    height : Annotated[float, Field(..., description= "Height of the Patient in meter", gt=0)]
    weight : Annotated[float, Field(..., description= "weight of the Patient in kg", gt=0)]

    @computed_field
    @property

    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
         if self.bmi < 18.5 :
                return 'Under Weight'
         elif self.bmi <25 :
             return 'Normal'
         elif self.bmi < 30:
             return 'Over weight'
         else :
             return 'obese'
   
class Patient_Update(BaseModel):
     name : Annotated[Optional[str], Field( description="Name Of the Patient ")] = None
     city: Annotated[Optional[str], Field( description="The city where Patient is living ")]= None
     age: Annotated[Optional[int], Field( description= "Age of the Patient", gt=0, lt=120)]= None
     height : Annotated[Optional[float], Field( description= "Height of the Patient in meter", gt=0)]= None
     weight : Annotated[Optional[float], Field( description= "weight of the Patient in kg", gt=0)]= None
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open('patient.json', 'w') as f:
         json.dump(data,f)

     
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

@app.post('/create')
def create_patient( patient : Patient):
    # Data Extraction
    data = load_data()

    # Cheking data is aready exist or not 
    if patient.id in data:
        raise HTTPException(status_code= 400, detail='Patient already exist')
    # Inserting new data 
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into json file 
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient Created Sucessfully'})
@app.put('/update/{patient_id}')
def update_patient(patient_id : str, patient_update: Patient_Update):
    data = load_data()
    if patient_id not in data :
        raise HTTPException(status_code= 404, detail="Patient Not Found")
    existing_info = data[patient_id]
    updated_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_info.items():
        existing_info[key] = value

    # exting info -> pydantic object -> because we want -> updated bmi + verdict
    existing_info['id']= patient_id   # adding id, Because Patient Model required id .
    existing_patient_object = Patient(**existing_info)

    # existing_patient_objec -> dict
    existing_info = existing_patient_object.model_dump(exclude='id')

    data[patient_id]= existing_info  
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Patient Updated Successfully'})  
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id :str):
    data = load_data()
    if patient_id not in data :
            raise HTTPException(status_code= 404, detail="Patient Not Found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Patient Deleted Successfully'})  


