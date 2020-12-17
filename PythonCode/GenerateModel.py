from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import bct
app = FastAPI()

def getStructuralnetwork(k, m, structure):
    if structure == "random":
        return bct.makerandCIJ_und(k, m)
    elif structure == "lattice":
        return bct.makeringlatticeCIJ(k, m)
    elif structure == "smallword":
        return None#TODO small world
    else:
        raise ValueError("Network type" + type + "not supported")



@app.get("/model/artificial/")
async def generateNetwork(nodes: int = 20, edges: int = 100, structure: str = "random"):
    # weighted undirected network
    model = getStructuralnetwork(nodes, edges, structure)
    # functionalConnectivity = bct.p
    print(type(model))
    listmodel = model.tolist()
    return listmodel

