var td = new Date();
td.setDate(td.getDate() -1);
td = td.toISOString().slice(0,10).replace('-','').replace('-','')
fileloc = "data/"+td+".locations.json"

d3.json(fileloc, function(error, json) {
    if (error) return console.warn(error);

    // Datamaps expect data in format:
    // { "USA": { "fillColor": "#42a844", numberOfWhatever: 75},
    //   "FRA": { "fillColor": "#8dc386", numberOfWhatever: 43 } }
    var series = json;
    // We need to colorize every country based on "numberOfWhatever"
    // colors should be uniq for every value.
    // For this purpose we create palette(using min/max series-value)
    var onlyValues = series.map(function(obj) {
        return obj[1];
    });
    var minValue = Math.min.apply(null, onlyValues),
        maxValue = Math.max.apply(null, onlyValues);
    // create color palette function
    // color can be whatever you wish
    var paletteScale = d3.scale.linear()
        .domain([minValue, maxValue])
        .range(["#EFEFFF", "#02386F"]); // blue color
    // fill dataset in appropriate format
    var dataset = {};
    series.forEach(function(item) { //
        // item example value ["USA", 70]
        var iso = item[0];
        var value = item[1];
        var u = item[2];
        dataset[iso] = {
            numberOfThings: value,
            fillColor: paletteScale(value),
            url1: u
        };
    });
    // render map
    new Datamap({
        element: document.getElementById('mapcontainer'),
        // projection: 'mercator', // big world map
        // countries don't listed in dataset will be painted with this color
        fills: {
            defaultFill: '#F5F5F5'
        },
        data: dataset,
        geographyConfig: {
            borderColor: '#DEDEDE',
            highlightBorderWidth: 2,
            // don't change color on mouse hover
            highlightFillColor: function(geo) {
                return geo['fillColor'] || '#F5F5F5';
            },
            // only change border
            highlightBorderColor: '#B7B7B7',
            // show desired information in tooltip
            popupTemplate: function(geo, data) {
                // don't show tooltip if country don't present in dataset
                if (!data) {
                    return;
                }
                // tooltip content
                return ['<div class="hoverinfo">',
                    '<strong>', geo.properties.name, '</strong>',
                    // '<br>Count: <strong>', data.numberOfThings, '</strong>',
                    '<br><a href="',data.url1,'">',data.url1,'</a>',
                    '</div>'
                ].join('');
            }
        }
    });
});
