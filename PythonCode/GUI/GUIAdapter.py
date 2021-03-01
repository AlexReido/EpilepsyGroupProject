#  TODO get json from adjacency
import json
from scipy import io
from fastapi import FastAPI
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

"""{
    "nodes": [
        {
          "id": "id1",
          "name": "name1",
          "val": 1
        },
        {
          "id": "id2",
          "name": "name2",
          "val": 10
        },
        (...)
    ],
    "links": [
        {
            "source": "id1",
            "target": "id2"
        },
        (...)
    ]
}"""
gui_adapter = FastAPI()
origins = [
    "http://127.0.0.1:60660/",
]

gui_adapter.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@gui_adapter.get("/")
def getNetwork():
    nodes = []
    edges = []
    adj_mat = io.loadmat('../resources/net.mat')
    adj_mat = adj_mat['net']
    print(type(adj_mat))
    for row in range(len(adj_mat)):
        # node object
        nodes.append({
            "id": row
        })

    for i, row in enumerate(adj_mat):
        for j, link in enumerate(row):
            if link > 0.008:
                edges.append({
                    "source" : i,
                    "target" : j,
                    "val" : link,
                })

    network = {"nodes": nodes, "links": edges}
    return json.dumps(network)


if __name__ == '__main__':
    print(getNetwork())
    server = threading.Thread(target=uvicorn.run("GUIAdapter:gui_adapter", host="127.0.0.1", port=5000, log_level="info"))
    server.start()

