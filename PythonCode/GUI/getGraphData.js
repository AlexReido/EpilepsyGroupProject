function getGraphData(adjacency, linkthreshold, json = true){
  // console.log(adjacency)
  if (json ==  true){
    var adj = JSON.parse(JSON.parse(adjacency));
  }else{
    var adj =JSON.parse(adjacency);
  }
  // console.log(adj)
  adjacency_matrix = adj;
  // document.getElementById("search_link").setAttribute("href","search.html & net="+adjacency_matrix);
  localStorage.setItem("net", JSON.stringify(adjacency_matrix));
  // console.log(adj);
  // console.log(typeof adj);
  // const adjacency = adjacency
  nodes = [];
  edges = [];
  adj.forEach(function (row, i) {
    // console.log(i)
    nodes.push({"id": i});
    row.forEach(function (link, j) {
      // console.log(i, j)
      if (link > linkthreshold){
        edges.push({
          "source": i,
          "target" : j,
          "val" : link,
        });
      }
    });
    i ++;
  });
  // console.log(nodes);
  // console.log(edges);
  return {"nodes": nodes, "links": edges};
}

module.exports = getGraphData;
