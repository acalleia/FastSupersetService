from fastapi import FastAPI
from mangum import Mangum
from app import database

app = FastAPI()


def configure():
    app.include_router(database.router)


configure()
if __name__ == '__main__':
    handler = Mangum(app)
