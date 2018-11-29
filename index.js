var margin = {
    top: 10,
    bottom: 10,
    left: 10,
    right:10
}, width = parseInt(d3.select('#viz').style('width'))
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
    .domain([118, 127])
    .range(d3.schemeReds[9]);

var countyColor = d3.scaleLinear()
    .domain([0, 5])
    .range(d3.schemeBlues[9]);


Promise.all([d3.json('data/us-counties.topojson'), d3.json('data/state_cancer_center.json'), d3.json('data/counties_cancer_data.json')])
    .then(([us, cancer_centers, counties_data]) => {
        ready(us, cancer_centers, counties_data)
    });

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}


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
var county_cancer_data = {};

function ready(us, cancer_centers, counties_data) {
    state_cancer_centers = cancer_centers;
    county_cancer_data = counties_data;
    g.append("g")
        .attr("id", "counties")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.counties).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", "county-boundary")
        .attr('fill', function(d) {
            const county_fips = pad(d.id, 5);
            const county_data = county_cancer_data[county_fips];
            if (county_data === undefined) return "black";
            let {breast_death_rate: br, cervical_death_rate: cr, colon_death_rate: cor, stomach_death_rate: sr} = county_data
            if (br === null) br = 0;
            if (cr === null) cr = 0;
            if (cor === null) cor = 0;
            if (sr === null) sr = 0;

            const total = parseFloat(br) + parseFloat(cr) + parseFloat(cor) + parseFloat(sr);
            return countyColor(total)
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
        .attr("d", path);

}


function drawChart(dataset, desc=[]) {

    let years = [...Array(16).keys()].map((x) => x + 2000);
    dataset = dataset.map((ds) => ds.map((x) => parseFloat(x.replace(',',''))));

    let domain_min = Number.POSITIVE_INFINITY;
    let domain_max = Number.NEGATIVE_INFINITY;

    for (let i=0; i< dataset.length; i++) {
        // console.log(i, dataset[i]);
        let current_min = Math.min(...dataset[i]);
        let current_max = Math.max(...dataset[i]);
        // console.log(current_min, current_max);
        if (current_min < domain_min)
            domain_min = current_min;
        if (current_max > domain_max)
            domain_max = current_max;
    }

    // console.log(domain_max, domain_min);

    var xScale = d3.scaleLinear()
        .domain([1999, 2016]) // input
        .range([0, width - margin.left*2.5]); // output

    var yScale = d3.scaleLinear()
        .domain([domain_min-100, domain_max+100]) // input
        .range([height/3, 0]); // output


    var line = d3.line()
        .x(function(d, i) {
            return xScale(years[i]);
        }) // set the x values for the line generator
        .y(function(d) {
            return yScale(d);
        }); // set the y values for the line generator

    let chartsvg = d3.select(".chart-viz").append("svg")
        .attr("width", width + margin.left + margin.right )
        .attr("height", height/3 + margin.top + margin.bottom)
        .attr('class', 'margin-top-bottom')
        .append("g")
        .attr("transform", "translate(" + margin.left*3 + "," + margin.top/3 + ")");

    chartsvg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + 0 + "," + height/3 + ")")
        .call(d3.axisBottom(xScale).tickFormat(d3.format("d"))); // Create an axis component with d3.axisBottom

// 4. Call the y axis in a group tag
    chartsvg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale).tickFormat(d3.format("d"))); // Create an axis component with d3.axisLeft

// 9. Append the path, bind the data, and call the line generator
    dataset.map((ds, i) => {
        chartsvg.append("path")
            .datum(ds) // 10. Binds data to the line
            .attr("class", "line") // Assign a class for styling
            .attr("d", line)
            .attr("stroke", desc[i].color);
    });

    const legend = d3.select(".chart-viz")
        .append('div')
        .attr("class", "legend");

    for (var y in desc) {
        console.log(y);
        series = legend.append('div');
        series.append('div').attr("class", "series-marker").style("background-color", desc[y].color)
            .append('p').text(desc[y].label);
    }


}

function clicked(d) {
    d3.select(".chart-viz")
        .selectAll("svg")
        .remove();

    d3.select(".chart-viz")
        .selectAll("div")
        .remove();

    if (d3.select('.background').node() === this) return reset();

    if (active.node() === this) return reset();

    let state_data = state_cancer_centers[d.id.toString()];
    // console.log(state_data);
    // console.log(state_data.mortality_by_year.Rate);

    let {RateFemale:mortalityFemale, RateMale:mortalityMale, RateTotal:mortalityTotal} = state_data.gender_mortality_by_year;
    let {RateWhite, RateOther, RateBlack, RateAll} = state_data.race_mortality_by_year;

    drawChart([mortalityFemale, mortalityMale, mortalityTotal], [
        {color: 'red', label: 'Female'},
        {color: 'blue', label: 'Male'},
        {color: 'black', label: 'Both'}
        ]);
    drawChart([RateWhite, RateOther, RateBlack, RateAll], [
        {color: 'red', label: 'White'},
        {color: 'blue', label: 'Other'},
        {color: 'black', label: 'Black'},
        {color: 'green', label: 'All'}
        ]);

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

    d3.select(".chart-viz")
        .selectAll("svg")
        .remove();

    d3.select(".chart-viz")
        .selectAll("div")
        .remove();

    g.transition()
        .delay(100)
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr('transform', 'translate('+margin.left+','+margin.top+')');

}