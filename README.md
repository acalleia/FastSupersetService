# FastSupersetService
The app retrieves data from the Service Now API and processes it through FastAPI to relay to Apache Superset. By doing this we can easily visualize the data provided and make better decisions on how to properly use Service Now.

## Local Installation 

```
# Set up Python 3.7 virtual environment
. service/bin/activate

# Install Dependencies
pip3 install -r requirements.txt
```
Apache Superset does not run on versions of Python newer than 3.7

## Running server

### Uvicorn web server
`uvicorn app.main:app --reload`

### Apache-Superset 
`superset run -p 8088 --with-threads --reload --debugger` <= Run in separate tab from web server

## Viewing Local SQLite3 database
```
sqlite3 servicenow.db
# Now inside sqlite CLI
sqlite3> select * from incidents
sqlite3> .exit
```
