from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import bct
app = FastAPI()

def getStructuralnetwork(k, m):
    return  bct.makerandCIJ_und(k, m)



@app.get("/")
async def root():
    # weighted undirected network
    model = bct.makerandCIJ_und(20, 100)
    # functionalConnectivity = bct.p
    print(type(model))
    bct.generative_model()
    return jsonable_encoder(model)