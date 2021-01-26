from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import bct
import numpy as np
import matlab.engine

app = FastAPI()


def getStructuralnetwork(k, m, structure):
    if structure == "random":
        return bct.makerandCIJ_und(k, m)
    elif structure == "lattice":
        return bct.makeringlatticeCIJ(k, m)
    elif structure == "toeplitz":
        return bct.maketoeplitzCIJ(k, m, 1.5)
    elif structure == "smallword":
        return True #TODO small world
    else:
        raise ValueError("Network type: " + type + "not supported")



@app.get("/model/artificial/")
async def generateNetwork(nodes: int = 20, edges: int = 100, structure: str = "random"):
    # weighted undirected network
    model = getStructuralnetwork(nodes, edges, structure)
    # functional = bct.motif3funct_bin(model)
    distance = bct.distance_wei_floyd(model, 'log')
    # print("ditancee:")
    # print(type(distance))
    # print(distance)
    # print("first")
    print(distance[2])
    print(model)
    max = np.amax(distance)
    # print(max)
    # transform = lambda x: x/max
    func = np.divide(distance, max)
    func = np.around(func, 3)
    # print(func)
    # eng = matlab.engine.start_matlab()
    # print(type(model))
    # print(type(func))
    # print(type(distance))
    # # SC FC ED pred_var model
    predvar = ['ED']#,'SPLwei_log','SI','T']
    # predvar = matlab.double(predvar)
    # bct.z
    # res = eng.predict_fc(matlab.double(model.tolist()), matlab.double(func.tolist()),
    #                      matlab.double(distance[2].tolist()), predvar, nargout=5)
    # print(res)
    # functionalConnectivity = bct.p
    # print(functional)
    # print(type(model))
    listmodel = func.tolist()
    return listmodel[2]

