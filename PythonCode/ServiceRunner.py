# import uvicorn
import numpy as np
import bct
# async def app(scope, receive, send):
#     ...

if __name__ == "__main__":
    model = bct.makerandCIJ_und(20, 100)
    # functionalConnectivity = bct.p
    print(type(model))
    m = np.count_nonzero(model)/2
    distance = bct.distance_bin(model)
    print(distance)
    # bct.
    synth = bct.generative_model(model, distance, m)

    print(synth)
    # TODO add weights
    # uvicorn.run("GenerateModel:app", host="127.0.0.1", port=5000, log_level="info")