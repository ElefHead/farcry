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
    .domain([70, 87])
    .range(d3.schemeReds[9]);

var countyColor = d3.scaleLinear()
    .domain([70, 87])
    .range(d3.schemeReds[9]);


var funding_means = ["46615.480769230766", "52589.192307692305", "60677.92307692308", "71232.71153846153", "68523.98076923077",
    "69293.96153846153", "68630.96153846153", "69027.15384615384", "68749.73076923077", "69824.13461538461", "71414.82692307692",
    "71389.32692307692", "71455.90384615384", "67251.80769230769", "68608.58853846151", "66643.44338461538"];



Promise.all([d3.json('data/us-counties.topojson'), d3.json('data/state_cancer_center.json'), d3.json('data/cancer_centers_list.json'), d3.json('data/counties_cancer_data.json')])
    .then(([us, cancer_centers, cancer_center_list, counties_data]) => {
        ready(us, cancer_centers, cancer_center_list, counties_data)
    });

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

var sl;


const projection = d3.geoAlbersUsa()
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
var isolated_cancer_centers = {};

var ccradius = 5;

function ready(us, cancer_centers, cancer_center_list, counties_data) {
    isolated_cancer_centers = cancer_center_list;
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
            let {all_death_rate: ar} = county_data;
            if (ar === null) ar = 0;

            return countyColor(ar)
        })
        .on("mousemove", function(d) {
            if (active.node() === this) return;
            let {id} = d;
            var html = "";
            const county_deets = county_cancer_data[pad(id, 5)];
            html += "<div class=\"tooltip_kv\">";
            html += "<span class=\"tooltip_key\">";
            html += county_deets.county_name;
            html += "</span>";
            html += "<span class=\"tooltip_value\">Deaths Rate: ";
            html += county_deets.all_death_rate;
            html += "</span>";
            html += "<br/><br/>Recent Trend: "+county_deets.all_recent_trend;
            html += "</div>";

            $("#tooltip-container").html(html);
            $(this).attr("fill-opacity", "0.8");
            $("#tooltip-container").show();

            // var coordinates = d3.mouse(this);

            var map_width = $('.viz')[0].getBoundingClientRect().width;

            if (d3.event.layerX < map_width / 2) {
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX + 15) + "px");
            } else {
                var tooltip_width = $("#tooltip-container").width();
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
            }
        })
        .on('mouseout', function () {
            $('#tooltip-container').hide();
            $(this).attr("fill-opacity", "1");
        })
        .on("click", reset);

    g.append("g")
        .attr("id", "states-white")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.states).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", function (d) {
            return "state-white state-white"+d.id;
        })
        // .attr('margin', 5)
        .attr('fill', "white")
        .attr('stroke', 'black')
        .on("mousemove", function(d) {
            if (active.node() === this) return;
            let {id} = d;
            const year = sl.getValue();
            const state_deets = state_cancer_centers[id.toString()];
            var html = "";

            html += "<div class=\"tooltip_kv\">";
            html += "<span class=\"tooltip_key\">";
            html += state_deets.state_name;
            html += "</span>";
            html += "<span class=\"tooltip_value\">Year: ";
            html += year;
            html += "</span>";
            html += "<br/><br/>Death Rate: " + state_deets.mortality_by_year.Rate[year - 2000];
            html += "<br/>Funding: " + state_deets.funding_by_year.TotalAmount[year - 2000];
            html += "</div>";

            $("#tooltip-container").html(html);
            // $(this).attr("fill-opacity", "0.8");
            $("#tooltip-container").show();

            // var coordinates = d3.mouse(this);

            var map_width = $('.viz')[0].getBoundingClientRect().width;

            if (d3.event.layerX < map_width / 2) {
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX + 15) + "px");
            } else {
                var tooltip_width = $("#tooltip-container").width();
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
            }
        })
        .on('mouseout', function () {
            $('#tooltip-container').hide();
            // $(this).attr("fill-opacity", "1");
        })
        .on("click", clicked);

    g.append("g")
        .attr("id", "states")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.states).features)
        .enter().append("path")
        .attr("d", path)
        .attr("class", "state")
        // .attr('margin', 5)
        .attr('fill', function (d) {
            let {id} = d;
            const state_deets = state_cancer_centers[id.toString()];
            if (state_deets === undefined) return color(0);
            const {mortality_by_year: myr} = state_deets;
            if (myr === undefined) {
                return 'gray';
            }
            let mortality = myr.Rate[0];
            if (mortality === undefined || mortality===null)
                return 'gray';
            return color(parseFloat(mortality));
        })
        .on("mousemove", function(d) {
            if (active.node() === this) return;
            let {id} = d;
            const year = sl.getValue();
            const state_deets = state_cancer_centers[id.toString()];
            var html = "";

            html += "<div class=\"tooltip_kv\">";
            html += "<span class=\"tooltip_key\">";
            html += state_deets.state_name;
            html += "</span>";
            html += "<span class=\"tooltip_value\">Year: ";
            html += year;
            html += "</span>";
            html += "<br/><br/>Death Rate: " + state_deets.mortality_by_year.Rate[year - 2000];
            html += "<br/>Funding (per $1000): " + state_deets.funding_by_year.TotalAmount[year - 2000];
            html += "</div>";

            $("#tooltip-container").html(html);
            $(this).attr("fill-opacity", "0.8");
            $("#tooltip-container").show();

            // var coordinates = d3.mouse(this);

            var map_width = $('.viz')[0].getBoundingClientRect().width;

            if (d3.event.layerX < map_width / 2) {
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX + 15) + "px");
            } else {
                var tooltip_width = $("#tooltip-container").width();
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
            }
        })
        .on('mouseout', function () {
            $('#tooltip-container').hide();
            $(this).attr("fill-opacity", "1");
        })
        .on("click", clicked);

    g.append("path")
        .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
        .attr("id", "state-borders")
        .attr("d", path)
        .attr('stroke', 'black');

    g.append('g')
        .attr("id", "cancer-centers")
        .selectAll(".center-dots")
        .data(cancer_center_list)
        .enter().append('a')
        .attr('href', function (d) {
            return d.link;
        })
        .attr('target', '_blank')
        .append('circle')
        .attr('class', 'center-dots')
        .attr('cx', function (d) {
            let {lat, long} = d;
            let coords = projection([long, lat]);
            return coords[0];
        })
        .attr('id', function (d) {
            return d.name;
        })
        .attr('cy', function(d) {
            let {lat, long} = d;
            let coords = projection([long, lat]);
            return coords[1];
        })
        .attr('fill', function(d) {
            let {type} = d;
            if (type === "Comp") {
                return '#08519c';
            }else if (type === "Clinical") {
                return '#6baedc';
            }else if (type === 'Basic'){
                return '#deebf7';
            }else {
                return 'black';
            }
        })
        .attr('year', function (d) {
            return d.year;
        })
        .attr('style', function (d) {
            let {year} = d;

            if (parseInt(year)<=2000)
                return 'display:block';
            else
                return 'display:none';

        })
        .attr('stroke', 'darkred')
        .attr('r', ccradius)
        .on("mousemove", function(d) {
            if (active.node() === this) return;
            var html = "";

            html += "<div class=\"tooltip_kv\">";
            html += "<span class=\"tooltip_key\">";
            html += d.name;
            html += "</span>";
            html += "<span class=\"tooltip_value\">";
            html += "Type: " + d.type;
            html += "</span>";
            html += "<br/><br/>Year designated: "+d.year;
            html += "<br/>Location: " + d.state_name;
            html += "<br/>Click to visit website";
            html += "</div>";

            $("#tooltip-container").html(html);
            $(this).attr("fill-opacity", "0.8");
            $("#tooltip-container").show();

            // var coordinates = d3.mouse(this);

            var map_width = $('.viz')[0].getBoundingClientRect().width;

            if (d3.event.layerX < map_width / 2) {
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX + 15) + "px");
            } else {
                var tooltip_width = $("#tooltip-container").width();
                d3.select("#tooltip-container")
                    .style("top", (d3.event.layerY + 15) + "px")
                    .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
            }
        })
        .on('mouseout', function () {
            $('#tooltip-container').hide();
            $(this).attr("fill-opacity", "1");
        });

        sl = $('#slider').slider({
            formatter: function (value) {
                return "Year: " + value;
            }
        })
        .on('slide', changeColor)
        .on('change', changeColor)
        .data('slider');

    var resized = false;

    function changeColor() {
        let year = sl.getValue();
        $(".main-year").text(year);
        g.selectAll('.center-dots')
            .attr('style', function(d) {
                let {year: nci_year} = d;
                if (nci_year <= year) {
                    return 'display:block';
                }else {
                    return 'display:none';
                }
            });

        g.selectAll('.state')
            .attr('fill', function(d) {
                let {id} = d;
                const state_deets = state_cancer_centers[id.toString()];
                if (state_deets === undefined) return color(0);
                const {mortality_by_year: myr} = state_deets;
                if (myr === undefined) {
                    return 'gray';
                }
                let mortality = myr.Rate[year - 2000];
                if (mortality === undefined || mortality===null)
                    return 'gray';
                return color(parseFloat(mortality));
            });
        if (resized) {
            resizeByFunding();
        }
    }

    function resizeByFunding(dur=0) {
        let year = sl.getValue();
        resized = true;
        g.selectAll('.state')
            .transition()
            .duration(dur)
            .attr("transform", function (d) {
                let {id} = d;
                const state_deets = state_cancer_centers[id.toString()];
                var centroid = path.centroid(d),
                    x = centroid[0],
                    y = centroid[1];
                if (isNaN(x) || isNaN(y))
                    return null;
                else {
                    let {state_name} = state_deets;
                    let {TotalAmount: funding} = state_deets.funding_by_year;
                    let {Rate: mortality_rate} = state_deets.mortality_by_year;
                    let fund = parseFloat(funding[year - 2000]);
                    let mrate = parseFloat(mortality_rate[year - 2000]);
                    if (fund === 0) {
                        return "translate(" + x + "," + y + ")"
                            + "scale(" + 0 + ")"
                            + "translate(" + -x + "," + -y + ")";
                    }
                    else {
                        // let index = fund / mrate;
                        // let scale_factor = index / 2362.209;
                        let scale_factor = fund / 447728.861;
                        if (isNaN(scale_factor)) {
                            return "translate(" + x + "," + y + ")"
                                + "scale(" + 0 + ")"
                                + "translate(" + -x + "," + -y + ")";
                        }
                        return "translate(" + x + "," + y + ")"
                            + "scale(" + scale_factor + ")"
                            + "translate(" + -x + "," + -y + ")";
                    }
                }
            });
    }

    function resetToOriginal() {
        resized = false;
        g.selectAll('.state')
            .transition()
            .duration(1000)
            .attr("transform", function(d) {
                var centroid = path.centroid(d),
                    x = centroid[0],
                    y = centroid[1];
                if (isNaN(x) || isNaN(y))
                    return null;
                else {
                    return "translate(" + x + "," + y + ")"
                        + "scale(" + 1 + ")"
                        + "translate(" + -x + "," + -y + ")";
                }
            });
    }

    d3.select('#resize')
        .on('click', function () {
            resizeByFunding(1000)
        });

    d3.select('#reset')
        .on('click', resetToOriginal);


}


function drawChart(dataset, uniq, desc=[], title='', range=null, description="") {

    let years = [...Array(16).keys()].map((x) => x + 2000);
    dataset = dataset.map((ds) => ds.map((x, i) => {
        if (x === null) {
            x = NaN;
        }
        if (isNaN(x)) {
                let j = i;
                while (isNaN(x) && j>0) {
                    x = ds[j - 1];
                    j -= 1;
                }
                j = ds.length;
                while (isNaN(x) && j<ds.length){
                    x = ds[j-1];
                    j += 1;
                }
        }
        return parseFloat(x.replaceAll(',',''))
    }));

    let domain_min = Number.POSITIVE_INFINITY;
    let domain_max = Number.NEGATIVE_INFINITY;

    if (range != null) {
        domain_min = range[0];
        domain_max = range[1];
    }

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


    var xScale = d3.scaleLinear()
        .domain([1999, 2016]) // input
        .range([0, width - margin.left*4]); // output

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

    d3.select(".chart-viz")
        .append("div")
        .attr('class', 'margin-top center-items')
        .append("h3")
        .text(title);

    d3.select(".chart-viz")
        .append("div")
        .attr("class", 'col-12 center-items')
        .append('p')
        .attr("class", "font_4")
        .text(description);

    d3.select('.chart-viz')
        .append("div")
        .attr('class', 'center-items')
        .append("p")
        .text("Click the labels to filter. Hover on points for details.");

    d3.select(".chart-viz")
        .append("div")
        .attr('id', 'charttip-container'+uniq)
        .attr('class', 'charttip-container');

    let chartsvg = d3.select(".chart-viz").append("svg")
        .attr("width", width + margin.left + margin.right )
        .attr("height", height/3 + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left*4.5 + "," + margin.top/3 + ")");

    chartsvg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + 0 + "," + height/3 + ")")
        .call(d3.axisBottom(xScale).tickFormat(d3.format("d"))); // Create an axis component with d3.axisBottom


    chartsvg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale).tickFormat(d3.format("d"))); // Create an axis component with d3.axisLeft


    dataset.map((ds, i) => {
        chartsvg.append("path")
            .datum(ds) // 10. Binds data to the line
            .attr("class", "line "+uniq+desc[i].color.replace("#")) // Assign a class for styling
            .attr("d", line)
            .attr("stroke", desc[i].color);

        chartsvg.selectAll(".dot"+i)
            .data(ds).enter()
            .append('circle')
            .attr("class", "dot " + uniq + desc[i].color.replace("#")) // Assign a class for styling
            .attr("cx", function(d, i) { return xScale(years[i]) })
            .attr("cy", function(d) { return yScale(d) })
            .attr("r", 3)
            .attr("fill", desc[i].color)
            .on("mousemove", function(d, index) {
                if (active.node() === this) return;

                var html = "";

                html += "<div class=\"tooltip_kv\">";
                html += "<span class=\"tooltip_key\">";
                html += desc[i].label;
                html += "</span>";
                html += "<span class=\"tooltip_value\">" + years[index] + ": ";
                html += d.toFixed(3);
                html += "";
                html += "</span>";
                html += "</div>";

                $("#charttip-container"+uniq).html(html);
                $(this).attr("fill-opacity", "0.8");
                $("#charttip-container"+uniq).show();

                // var coordinates = d3.mouse(this);

                var map_width = $('.chart-viz')[0].getBoundingClientRect().width;

                if (d3.event.layerX < map_width / 2) {
                    d3.select("#charttip-container"+uniq)
                        .style("top", (d3.event.layerY + 15) + "px")
                        .style("left", (d3.event.layerX + 15) + "px");
                } else {
                    var tooltip_width = $("#charttip-container"+uniq).width();
                    d3.select("#charttip-container"+uniq)
                        .style("top", (d3.event.layerY + 15) + "px")
                        .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
                }
            })
            .on('mouseout', function () {
                $('#charttip-container'+uniq).hide();
            });
    });

    const legend = d3.select(".chart-viz")
        .append('div')
        .attr("class", "legend");

    for (var y in desc) {
        series = legend.append('div');
        series.append('div').attr("class", "series-marker " + "series-marker"+uniq+desc[y].color.replace("#")).style("background-color", desc[y].color)
            .on('click', function() {
                let selector = '.'+$(this).attr('class').replaceAll('series-marker', '').trim();
                if($(selector).css('display') !== 'none') {
                    $(selector).css('display', 'none')
                }else{
                    $(selector).css('display', 'inline')
                }
            })
            .append('p').text(desc[y].label);
    }


}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function clicked(d) {

    if (d===undefined) {
        return null;
    }


    $('.viz-buttons').css('display', 'none');
    $('#scroll-text').css('display', 'block');

    $('#counties').css('display', 'block');
    $('.state-white').css('display', 'block');
    $('.state-white'+d.id).css('display', 'none');
    $('.state').css('display', 'none');
    d3.select(".chart-viz")
        .selectAll("svg")
        .remove();

    d3.select(".chart-viz")
        .selectAll("div")
        .remove();

    g.selectAll('.center-dots')
        .attr('style', 'display:block');

    if (d3.select('.background').node() === this) return reset();

    if (active.node() === this) return reset();

    let state_data = state_cancer_centers[d.id.toString()];

    $('#map-tag').html(
        "5 year average age-adjusted death rate for each county in <b>"+state_data.state_name+"</b> over the years (2012 - 2017)"
    );
    // console.log(state_data);
    // console.log(state_data.mortality_by_year.Rate);

    let {RateFemale:mortalityFemale, RateMale:mortalityMale, RateTotal:mortalityTotal} = state_data.gender_mortality_by_year;
    let {RateWhite, RateOther, RateBlack, RateAll} = state_data.race_mortality_by_year;
    let {TotalAmount} = state_data.funding_by_year;

    drawChart([mortalityFemale, mortalityMale, mortalityTotal],
        'gender',
        [
            {color: '#CC79A7', label: 'Female'},
            {color: '#56B4E9', label: 'Male'},
            {color: '#000000', label: 'Mean'}
        ], 'Gender based Age-Adjusted Death Rates',
        null,
        "This graph plots the gender-wise age-adjusted death rate per 100,000 people over the years 2000 - 2015 in "+state_data.state_name+".");
    drawChart([RateWhite, RateBlack, RateOther, RateAll],
        'ethnicity',
        [
            {color: '#DA2C7F', label: 'Caucasian'},
            {color: '#0072B2', label: 'African-American'},
            {color: '#E69F00', label: 'Other'},
            {color: '#000000', label: 'Mean'}
        ],
        'Race-Ethnicity based Age-Adjusted Death Rates',
        null,
        "This graph plots the age-adjusted death rate per 100,000 people by ethnicity over 2000 - 2015 in "+state_data.state_name+".");

    drawChart([TotalAmount, funding_means], 'funding_data',
        [
            {color: '#009E73', label: state_data.state_name},
            {color: '#000000', label: "Mean"}
        ],
        "Total Fund Amounts",
        [10000, 700000],
        "This graph plots state funding and mean funding amounts per $1,000 over 2000 - 2015 for "+state_data.state_name+".");

    active.classed("active", false);
    active = d3.select(this).classed("active", true);

    var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

    g.selectAll('.center-dots')
        .transition()
        .duration(750)
        .attr("r", 3.5/scale);


    g.transition()
        .duration(750)
        .style("stroke-width", 1.5 / scale + "px")
        .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
}


function reset() {
    $('#counties').css('display', 'none');
    $('.state-white').css('display', 'block');
    $('.viz-buttons').css('display', 'block');
    $('.state').css('display', 'block');
    $('#scroll-text').css('display', 'none');
    active.classed("active", false);
    active = d3.select(null);

    $('#map-tag').html(
        "age-adjusted death rate for each state for each year"
    );
    d3.select(".chart-viz")
        .selectAll("svg")
        .remove();

    d3.select(".chart-viz")
        .selectAll("div")
        .remove();

    let year = sl.getValue();
    g.selectAll('.center-dots')
        .attr('style', function(d) {
            let {year: nci_year} = d;
            if (nci_year <= year) {
                return 'display:block';
            }else {
                return 'display:none';
            }
        });

    g.transition()
        .delay(100)
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr('transform', 'translate('+margin.left+','+margin.top+')');

    g.selectAll('.center-dots')
        .transition()
        .duration(750)
        .attr("r", ccradius);

}