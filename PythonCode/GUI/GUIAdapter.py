#  TODO get json from adjacency
import json
from scipy import io
from fastapi import FastAPI
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from PythonCode.GenerateArtificial.GenerateModel import get_artificial_net
from PythonCode.Search import SimulateDynamics
from PythonCode.Search.SearchNetwork import SearchNetwork

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

def getJsonfromAdj(adj_mat, link_threshold=0.008):
    """
    The link threshold is the minimum value for the edge
    weight to  be included in the graph for the client.
    :param adj_mat:
    :param link_threshold:
    :return:
    """
    nodes = []
    edges = []
    for row in range(len(adj_mat)):
        # node object
        nodes.append({
            "id": row
        })
    #TODO parametert
    for i, row in enumerate(adj_mat):
        for j, link in enumerate(row):
            if link > link_threshold:
                edges.append({
                    "source" : i,
                    "target" : j,
                    "val" : link,
                })

    network = {"nodes": nodes, "links": edges}
    return json.dumps(network)


@gui_adapter.get("/")
def getNetwork(artificial: bool = False, nodes: int = 20, edges: int = 100, structure: str = "random"):
    if artificial:
        art_mat = get_artificial_net(nodes, edges, structure)
        return json.dumps(art_mat.tolist())#getJsonfromAdj(art_mat)
    else:
        default_mat = io.loadmat('../resources/net.mat')
        default_mat = default_mat['net']
        # print(default_mat)
        return json.dumps(default_mat.tolist())  #getJsonfromAdj(default_mat)

def openNet(filename: str):
    pass


@gui_adapter.get("/search/")
def getSearchStatus(jsonNet, nodelist: list = []):
    # TODO import json or filename??
    t = 4000  # TODO for testing only
    if not nodelist:
        print("Searching whole network")

    else:
        print("evaluating the selection")
        network = openNet(fileName)
        coupling_ref, _, _ = SimulateDynamics.bni_find(network, t)
        result = SimulateDynamics.fitness_function([nodelist], coupling_ref, network, t)
        print(result)

        return json.dumps(result)


if __name__ == '__main__':

    print(getNetwork())
    server = threading.Thread(target=uvicorn.run("GUIAdapter:gui_adapter", host="127.0.0.1", port=5000, log_level="info"))
    server.start()

