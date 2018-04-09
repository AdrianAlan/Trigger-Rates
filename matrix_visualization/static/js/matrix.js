var margin = {top: 300, right: 0, bottom: 0, left: 300},
    width = 960,
    height = width,
    colorNegative = "#1A237E",
    colorNeutral = "#F5F5F5",
    colorPositive = "#B71C1C";

var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),
    c = d3.scale.category10().domain(d3.range(10));

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
   .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var colorMapNegative = d3.scale.linear()
	.domain([0.0,-1.0])
	.range([colorNeutral, colorNegative]);

var colorMapPositive = d3.scale.linear()
	.domain([0.0,1.0])
	.range([colorNeutral, colorPositive]);

var url = new URL (window.location.href);
var rm = url.searchParams.get("rm") | "0";
var fd = url.searchParams.get("fd") | "0";
var lr = url.searchParams.get("lr") | "0";

var load_file = "data/data" + rm + fd + lr + ".json";

console.log("Trying to load: " + load_file);

d3.json(load_file, function(data) {
    
    var matrix = [],
        nodes = data.nodes,
        n = nodes.length;

    nodes.forEach(function(node, i) {
        node.index = i;
        matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
    });

    data.links.forEach(function(link) {
        matrix[link.source][link.target].z = link.value;
        matrix[link.target][link.source].z = link.value;
    });
  
    var orders = {
        name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
        cluster: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
    };
    x.domain(orders.name);

    svg.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

    var row = svg.selectAll(".row")
        .data(matrix)
        .enter().append("g")
        .attr("class", "row")
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
        .each(row);

    row.append("line")
        .attr("x2", width);

    row.append("text")
        .attr("x", -6)
        .attr("y", x.rangeBand() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text(function(d, i) { return nodes[i].name; });

    var column = svg.selectAll(".column")
        .data(matrix)
        .enter().append("g")
        .attr("class", "column")
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

    column.append("line")
        .attr("x1", -width);

    column.append("text")
        .attr("x", 6)
        .attr("y", x.rangeBand() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "start")
        .text(function(d, i) { return nodes[i].name; });

    // Fix legend
    var key = d3.select("#legend")
        .append("svg")
        .attr("width", 960)
        .attr("height", 50);

    var legend = key.append("defs")
        .append("svg:linearGradient")
        .attr("id", "gradient")
        .attr("x1", "0%")
        .attr("y1", "100%")
        .attr("x2", "100%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

    legend.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", colorPositive)
        .attr("stop-opacity", 1);

    legend.append("stop")
        .attr("offset", "50%")
        .attr("stop-color", colorNeutral)
        .attr("stop-opacity", 1);

    legend.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", colorNegative)
        .attr("stop-opacity", 1);

    key.append("rect")
        .attr("width", 950)
        .attr("height", "100%")
        .style("fill", "url(#gradient)")
        .attr("transform", "translate(5, 20)");

    var y = d3.scale.linear()
        .range([950, 0])
        .domain([-1.0, 1.0]);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("bottom");

    key.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(5, 20)")
        .call(yAxis)

    function row(row) {
        var cell = d3.select(this).selectAll(".cell")
            .data(row.filter(function(d) { return d.z; }))
            .enter().append("rect")
            .attr("class", "cell")
            .attr("x", function(d) { return x(d.x); })
            .attr("width", x.rangeBand())
            .attr("height", x.rangeBand())
            .style("fill", function(d) {
                return d.z > 0 ? colorMapPositive(d.z) : colorMapNegative(d.z);
            })
            .on("mouseover", mouseover)
            .on("mouseout", mouseout);
    }

    function mouseover(p) {
        document.getElementById("details").innerHTML =
            "<p><i>Covariance details</i>" +
            "<p><b>" + nodes[p.x].name + "</b>" +
            "<img width='300px' src='figures/" +nodes[p.x].name + ".png'>" +
            "<p><b>" + nodes[p.y].name + "</b>" +
            "<img width='300px' src='figures/" +nodes[p.y].name + ".png'>" +
            "<p style='font-size: 40px;'> <b>" + Math.round(p.z * 100) / 100 + "</b>";

        d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
        d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
    }

    function mouseout() {
        d3.selectAll("text").classed("active", false);
    }

    d3.select("#cluster").on("change", function() {
        order(this.value);
    });

    function order(value) {
        x.domain(orders[value]);
        var t = svg.transition().duration(2000);

        t.selectAll(".row")
            .delay(function(d, i) { return x(i) * 4; })
            .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
            .selectAll(".cell")
            .delay(function(d) { return x(d.x) * 4; })
            .attr("x", function(d) { return x(d.x); });

        t.selectAll(".column")
            .delay(function(d, i) { return x(i) * 4; })
            .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
    }
});
