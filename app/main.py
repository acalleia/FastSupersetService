# importing dependancies & other files
from fastapi import FastAPI
from mangum import Mangum
from app import database

app = FastAPI()

# using database


def configure():
    app.include_router(database.router)


# using Mangum
configure()
if __name__ == '__main__':
    handler = Mangum(app)
