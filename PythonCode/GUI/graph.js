function updateSelectedList(selectedNodes){
  var node_list = "Selected nodes: <br />";
  for (var n of selectedNodes.values()){
    console.log(String(n.id));
    let val = String(n.id)+ "<br />"; //+ "<br />"
    node_list = node_list + val;
  }
  document.getElementById("left").innerHTML = node_list;
}

function saveNet(){
  // TODO if null
  let data = JSON.stringify(adjacency_matrix);
  // fs.writeFileSync('net.json', data);
  function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }
  console.log(data);
  download(data, 'json.txt', 'text/plain');
  // var csvfile = new Blob(data);
  // console.log(csvfile);
  // downloadBlob(csvfile, 'network.json');

}

function getGraphData(adjacency, linkthreshold, json = true){
  // console.log(adjacency)
  if (json ==  true){
    var adj = JSON.parse(JSON.parse(adjacency));
  }else{
    var adj =JSON.parse(adjacency);
  }
  console.log(adj)
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
  console.log(nodes);
  console.log(edges);
  return {"nodes": nodes, "links": edges};
}

function getnet(params = "") {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log("recieved network!");
      var graphdata = getGraphData(this.responseText, 0.008);
      console.log("json==", graphdata);
      // console.log(graphdata.nodes)
      displaygraph(graphdata);
    }
  };
  var url = "http://127.0.0.1:5000" + params
  xhttp.open("GET", url, true);
  xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
  xhttp.send();
}

// var net = getnet();
function displaygraph(graphData){
  const selectedNodes = new Set();
  updateSelectedList(selectedNodes);
   // const highlightLinks = new Set();
  let hoverNode = null;
  var graphElem = document.getElementById('3d-graph');
  var graphHeight = graphElem.getBoundingClientRect().height;
  var graphWidth = graphElem.getBoundingClientRect().width;
  console.log(graphHeight)
  const graph = ForceGraph3D() // should be const
    (graphElem)
      // .nodeColor(node => 'rgb(255,0,111,1)')
      // pink = 'rgb(255,0,255,0.7)'
      // orange = 'rgba(219,131,16,0.7)'
      // blue = 'rgb(0,0,170,0.7)'
      // red = 'rgb(255,51,51,0.7)'
      // left selected and right normal
      .height('600') //String(graphHeight))
      .width('900')  //String(graphWidth))
      .nodeColor(node =>selectedNodes.has(node) ? 'rgb(255,10,10,0.8)': 'rgb(0,0,170,0.7)')
      // .nodeOpacity(1)
      .nodeLabel(d => `<span style="font-size: 170%; color: #01653A; font-weight: bold;">${d.id}</span>`)
      // .onNodeHover(node => elem.style.cursor = node ? 'pointer' : null)
      // .nodeThreeObject(node => {
      //   const sprite = new SpriteText(node.id);
      //   sprite.material.depthWrite = false; // make sprite background transparent
      //   sprite.color = node.color;
      //   sprite.textHeight = 8;
      //   return sprite;
      // })
      .enableNodeDrag(false)
      // purple 'rgba(124,21,65,1)'
      .linkColor(link => 'rgba(30,30,30,0.3)')
      // link width is very slow
      // .linkWidth(0.5)
      .linkOpacity(1)
      // .width(1200)
      // .height(800)
      .onNodeClick((node, event) => {
          if (event.ctrlKey || event.shiftKey || event.altKey) { // multi-selection
            selectedNodes.has(node) ? selectedNodes.delete(node) : selectedNodes.add(node);
          } else { // single-selection
            const untoggle = selectedNodes.has(node) && selectedNodes.size === 1;
            selectedNodes.clear();
            !untoggle && selectedNodes.add(node);
          }
          graph.nodeColor(graph.nodeColor()); // update color of selected nodes
          updateSelectedList(selectedNodes);
      })
      .graphData(graphData);
  graph.renderer().setClearColor( 0x000000, 0 );
  graph.backgroundColor('#FFFFFF');

  function updateHighlight() {
    // trigger update of highlighted objects in scene
    graph
      .nodeColor(graph.nodeColor())
      // .linkWidth(Graph.linkWidth())
      // .linkDirectionalParticles(Graph.linkDirectionalParticles());
  }
  function resetView() {
    graph.zoomToFit(400)
    // graph.onEngineStop(() => );
  }
  var button = document.getElementById("btn_reset");
  button.onclick = function(){resetView()};

  var element = document.getElementById('3d-graph')

}

function getart(){

  nodes = document.getElementById("nodes").value;
  edges = document.getElementById("edges").value;
  console.log(nodes);
  console.log(edges);
  let extraparam = ""
  if (nodes !== null) {
    extraparam = extraparam + "&nodes=" + nodes.toString()
  }
  if (edges !== null) {
    extraparam = extraparam + "&edges=" + edges.toString()
  }
  getnet('?artificial=True'+ extraparam);
}

// const openNet = document.querySelector('input[type="file"]')
// openNet.addEventListener('change', function(e) {
//   console.log(openNet.files[0])
// })

export {  saveNet, getnet, getart } from './graph.js';
