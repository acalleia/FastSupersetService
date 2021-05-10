# importing dependancies & other files
from fastapi import FastAPI
from typing import List, Optional
import databases
import sqlalchemy
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from fastapi import APIRouter
import httpx

# Initialize database
DATABASE_URL = "sqlite:///./servicenow.db"


database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create table
incidents = sqlalchemy.Table(

    "incidents",

    metadata,

    sqlalchemy.Column("number", sqlalchemy.String, primary_key=True),

    sqlalchemy.Column("category", sqlalchemy.String),

    sqlalchemy.Column("impact", sqlalchemy.Numeric),

    sqlalchemy.Column("urgency", sqlalchemy.Numeric),

    sqlalchemy.Column("priority", sqlalchemy.Numeric),

    sqlalchemy.Column("description", sqlalchemy.String)

)

# Start engine
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

# create table models


class Incident(BaseModel):
  # __tablename__ = "incidents"
    number: str
    category: Optional[str] = None
    impact: Optional[int] = None
    urgency: Optional[int] = None
    priority: Optional[int] = None
    description: Optional[str] = None


class Newincident (BaseModel):
    number: Optional[str] = None


class Removeincident (BaseModel):
    number: Optional[str] = None


app = FastAPI()


router = APIRouter()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Create routes


@router.get("/incidents", response_model=List[Incident])
async def read_incidents():
    query = incidents.select()
    return await database.fetch_all(query)


@router.delete("/incidents", response_model=Incident)
async def remove_incident(number: str):
    query = incidents.delete().where(incidents.c.number == number)
    await database.execute(query)
    return {incidents.dict()}
    # return {**incident.dict(), "id": last_record_id}

# Make API call to Service Now API and post to DB


@router.post('/incidents', response_model=Incident)
# async def acquire_service_now_data(incident: Incident = fastapi.Depends()):
async def acquire_service_now_data():
    url = "https://dev105142.service-now.com/api/now/table/incident?sysparm_fields=number%2Ccategory%2Cimpact%2Curgency%2Cpriority%2Cdescription&sysparm_limit=500"

    user = 'Admin'
    pwd = 'tpK2nRiCiKE9'

    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=(user, pwd), headers=headers)
        response.raise_for_status()
        data = response.json()

    result = data.get('result', {})
    for r in result:
        query = incidents.insert().values(number=r["number"], category=r["category"], impact=r["impact"],
                                          urgency=r["urgency"], priority=r["priority"], description=r["description"]).prefix_with('OR IGNORE')
        await database.execute(query)
