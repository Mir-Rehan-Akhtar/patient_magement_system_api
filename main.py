from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data
     

