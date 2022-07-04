import numpy
import pandas
import psycopg2
from table import returnTable, returnFreq



from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Datatable(BaseModel):
    name: str
    column: str

#@app.get("/", response_class=HTMLResponse)
#async def root():
#    return html

tableName = "chicagodata"

@app.post("/testlink", response_class=HTMLResponse)
def setTableName(tab: Datatable):
    tableName = tab.name
    return returnTable(tableName)

@app.get("/testlink", response_class=HTMLResponse)
def htmlReturn():
    return returnTable(tableName)

@app.post("/freqpost", response_class=HTMLResponse)
def freqReturn(tab: Datatable):
    return returnFreq(tab.name, tab.column)

#the fastAPI is a big work in progress
#remember to do $ uvicorn main:app --reload
#access on http://127.0.0.1:8000/testlink
