if (document.getElementById('entity_graph') != null) {
  var graph_data_file = document.getElementById("entity_graph").getAttribute("file");
  console.log(graph_data_file)

  var width = 1200,
  height = 1200;

  var color = d3.scale.category20();

  var force = d3.layout.force()
  .charge(-300)
  .linkDistance(400)
  .size([width, height]);

  var svg = d3.select("#entity_graph").append("svg")
  .attr("width", width)
  .attr("height", height);

  d3.json(graph_data_file, function(error, graph) {
    force
    .nodes(graph.nodes)
    .links(graph.links)
    .start();

    var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 10)
    .attr("r", function(d){ size = d.size; if(size >= 30){size = 30;} return size;})
    .style("fill", function(d) { if(d.group == 1){ return "blue"; } if(d.group == 2){ return "orange"; } if(d.group == 3){ return "green"; }})
    .style("cursor","move")
    .call(force.drag);

    var texts = svg.selectAll("text.label")
    .data(graph.nodes)
    .enter().append("text")
    .attr("class", "label")
    .attr("fill", "black")
    .on("click", function(d) { window.open(d.url); })
    .style("cursor","pointer")
    .text(function(d) {  return d.name;  });

    node.append("title")
    .text(function(d) { return d.name; });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });

      texts.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";});
    });
  });
}
