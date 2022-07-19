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

class Connection(BaseModel):
    host: str
    database: str
    user: str
    password: str


#@app.get("/", response_class=HTMLResponse)
#async def root():
#    return html

tableName = "chicagodata"
conn = Connection
conn.host = "localhost"
conn.database = "postgres"
conn.user = "postgres"
conn.password = "sq39iaiu"

@app.post("/changedb")
def setNewDB(dbconn: Connection, response_class=HTMLResponse):
    conn.host = dbconn.host
    conn.database = dbconn.database
    conn.user = dbconn.user
    conn.password = dbconn.password
    return returnTable(tableName, conn.host, conn.database, conn.user, conn.password)

@app.post("/testlink", response_class=HTMLResponse)
def setTableName(tab: Datatable):
    tableName = tab.name
    return returnTable(tableName, conn.host, conn.database, conn.user, conn.password)

@app.get("/testlink", response_class=HTMLResponse)
def htmlReturn():
    return returnTable(tableName, conn.host, conn.database, conn.user, conn.password)

@app.post("/freqpost", response_class=HTMLResponse)
def freqReturn(tab: Datatable):
    return returnFreq(tab.name, tab.column, conn.host, conn.database, conn.user, conn.password)

#the fastAPI is a big work in progress
#remember to do $ uvicorn main:app --reload
#access on http://127.0.0.1:8000/testlink
