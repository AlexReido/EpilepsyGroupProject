import uvicorn
import requests
import asyncio
from multiprocessing import Process
import threading
import numpy as np
import bct
# async def app(scope, receive, send):
#     ...

if __name__ == "__main__":

    # functionalConnectivity = bct.p
    # print(type(model))
    # m = np.count_nonzero(model)/2
    # distance = bct.distance_bin(model)
    # print(distance)
    # s =
    # synth = bct.generative_model(model, distance, m)

    # print(synth)
    # TODO add weights
    #Get /model/artificial/?type=Random&nodes=20&edges=100
    # proc = Process(target=uvicorn.run,
    #                     args=('GenerateModel:app',),
    #                     kwargs={
    #                         "host": "127.0.0.1",
    #                         "port": 5000,
    #                         "log_level": "info"},
    #                     daemon=True)
    # proc.start()
    # asyncio.sleep(0.1)
    server = threading.Thread(target=uvicorn.run("GenerateModel:app", host="127.0.0.1", port=5000, log_level="info"))
    server.start()


