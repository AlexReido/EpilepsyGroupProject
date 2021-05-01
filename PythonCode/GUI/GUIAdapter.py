#  TODO get json from adjacency
import json
# from scipy import io
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from PythonCode.GenerateArtificial.GenerateModel import get_artificial_net
from PythonCode.Search.SearchNetwork import SearchNetwork

gui_adapter = FastAPI()
searchThreads = []
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
    # TODO parametert
    for i, row in enumerate(adj_mat):
        for j, link in enumerate(row):
            if link > link_threshold:
                edges.append({
                    "source": i,
                    "target": j,
                    "val": link,
                })

    network = {"nodes": nodes, "links": edges}
    return json.dumps(network)


@gui_adapter.get("/")
def getNetwork(artificial: bool = False, nodes: int = 20, edges: int = 100, structure: str = "random"):
    if artificial:
        art_mat = get_artificial_net(nodes, edges, structure)
        return json.dumps(art_mat.tolist())  # getJsonfromAdj(art_mat)
    else:
        default_mat = io.loadmat('../resources/net.mat')
        default_mat = default_mat['net']
        # print(default_mat)
        return json.dumps(default_mat.tolist())  # getJsonfromAdj(default_mat)


def openNet(filename: str):
    pass


class SearchRequest(BaseModel):
    filename: str
    adj_mat: list
    node_list: list
    n_gens: int
    max_nodes: int


class SearchThread():
    def __init__(self, threadFunction, config: SearchRequest, client):
        self.threadFunction = threadFunction
        self.config = config
        self.thread = None
        self.finished = False
        self.result = {}
        self.client = client

    def run_thread(self):
        print("HERE")
        print(self.threadFunction)
        print("running with ", self.config.n_gens)
        thread = threading.Thread(target=self.threadFunction(self.config.n_gens, self.config.max_nodes, self), args=())
        self.thread = thread

    def getStatus(self):
        if self.finished:
            return {"finished": True, "results":self.result}
        else:
            # if self.result == {}:
            #     return {"finished": False, "results": "initialising"}
            # else:
            return {"finished": False, "results": self.result}

    def returnResults(self, results):
        self.finished = True
        url = "http://" + str(self.client.host) + ":" + str(self.client.port)
        print("URl ", url)
        out = [list(val) for val in list(results.F)]
        input = [[bool(x) for x in list(val)] for val in list(results.X)]
        print(out)
        print(input)
        requests.post(url, data=json.dumps({"out":out, "in":input}))
        # current error is that the client refuses as we aren't listening from the js
        # TODO maybe easier just to poll from client

# @gui_adapter.get("/search/")
# def getAllSearches():
#     """:returns all of the previous search requests"""
#     searches = []
#     for search in searchThreads:
#         searches.append(search.config.filename)
#     return json.dumps(searches)


@gui_adapter.get("/search/")
def getSearchStatus(filename: str):
    print("Getting search status")
    print(searchThreads)
    for search in searchThreads:
        print(search.config.filename)
        if search.config.filename == filename:
            return json.dumps(search.getStatus())
    return json.dumps(False) # 404


@gui_adapter.post("/search/")
def startSearch(search_config: SearchRequest, request: Request):
    client = request.client
    print("hose: ", client.host)
    print("port: ", client.port)
    print("Name: ", search_config.filename)
    print("n_gens: ", search_config.n_gens)
    print("max_nodes: ", search_config.max_nodes)
    print("node_list: ", search_config.node_list)
    print("Adj_mat: ", search_config.adj_mat)

    if search_config.node_list == []:
        print("Searching whole network")
        searcher = SearchNetwork("NSGA2", network=search_config.adj_mat, timesteps=4000)
        # searchFunction =
        searchthread = SearchThread(searcher.search, search_config, client)
        searchThreads.append(searchthread)
        searchthread.run_thread()



    else:
        print("evaluating the selection")
        # network = openNet(fileName)
        # coupling_ref, _, _ = SimulateDynamics.bni_find(network, t)
        # result = SimulateDynamics.fitness_function([nodelist], coupling_ref, network, t)
        # print(result)
        #
        # return json.dumps(result)


class Item(BaseModel):
    matfile: str


from PythonCode.ImportIEEG.Import import *


@gui_adapter.post("/ieeg")
def convertIeeg(item: Item):
    return json.dumps(get_adjacency(item.matfile))


if __name__ == '__main__':
    print(getNetwork())
    server = threading.Thread(
        target=uvicorn.run("GUIAdapter:gui_adapter", host="127.0.0.1", port=5000, log_level="info"))
    server.start()
