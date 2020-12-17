from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
app = FastAPI()


@app.get("/")
async def root():
    model = []
    return jsonable_encoder(model)