var margin = {
    top: 10,
    bottom: 10,
    left: 10,
    right:10
}, width = parseInt(d3.select('.viz').style('width'))
    , width = width - margin.left - margin.right
    , mapRatio = 0.5
    , height = width * mapRatio
    , active = d3.select(null);

var svg = d3.select('.viz').append('svg')
    .attr('class', 'center-container')
    .attr('height', height + margin.top + margin.bottom)
    .attr('width', width + margin.left + margin.right);

svg.append('rect')
    .attr('class', 'background center-container')
    .attr('height', height + margin.top + margin.bottom)
    .attr('width', width + margin.left + margin.right)
    .on('click', clicked);

var color = d3.scalePow()
    .domain([118, 200])
    .range(d3.schemeReds[9]);


Promise.all([d3.json('data/us-counties.topojson'), d3.json('data/state_cancer_center.json')])
    .then(([us, cancer_centers]) => {
        ready(us, cancer_centers)
    });

var projection = d3.geoAlbersUsa()
    .translate([width /2 , height / 2])
    .scale(width);

var path = d3.geoPath()
    .projection(projection);

var g = svg.append("g")
    .attr('class', 'center-container center-items us-state')
    .attr('transform', 'translate('+margin.left+','+margin.top+')')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom);

var state_cancer_centers = {};

function ready(us, cancer_centers) {
    state_cancer_centers = cancer_centers;
    g.append("g")
        .attr("id", "counties")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.counties).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", "county-boundary")
        .attr('fill', function(d) {
            console.log(d);
        })
        .on("click", reset);

    g.append("g")
        .attr("id", "states")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.states).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", "state")
        .attr('margin', 5)
        .attr('fill', function (d) {
            if (d !== null) {
                let {id} = d;
                const state_deets = state_cancer_centers[id.toString()];
                console.log(state_deets === undefined);
                if (state_deets === undefined) return color(0);
                let mortality = state_deets.mortality;
                if (mortality === undefined)
                    return 'gray';
                return color(parseFloat(state_deets.mortality));
            }else {
                return color(0);
            }
        })
        .on("click", clicked);


    g.append("path")
        .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
        .attr("id", "state-borders")
        .attr("d", path)
        .attr('transform', function(d) {
            console.log(d);
        });

}

function clicked(d) {
    if (d3.select('.background').node() === this) return reset();

    if (active.node() === this) return reset();

    active.classed("active", false);
    active = d3.select(this).classed("active", true);

    var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

    g.transition()
        .duration(750)
        .style("stroke-width", 1.5 / scale + "px")
        .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
}


function reset() {
    active.classed("active", false);
    active = d3.select(null);

    g.transition()
        .delay(100)
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr('transform', 'translate('+margin.left+','+margin.top+')');

}