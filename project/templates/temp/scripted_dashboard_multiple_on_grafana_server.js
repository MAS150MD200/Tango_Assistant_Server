/* global _ */

/*
 * Complex scripted dashboard
 * This script generates a dashboard object that Grafana can load. It also takes a number of user
 * supplied URL parameters (int ARGS variable)
 *
 * Return a dashboard object, or a function
 *
 * For async scripts, return a function, this function must take a single callback function as argument,
 * call this callback function with the dashboard object (look at scripted_async.js for an example)
 */



// accessable variables in this scope
var window, document, ARGS, $, jQuery, moment, kbn;

// Setup some variables
var dashboard;

// All url parameters are available via the ARGS object
var ARGS;

// Intialize a skeleton with nothing but a rows array and service object
dashboard = {
  rows : [],
};

// Set a title
dashboard.title = 'Graphite Metrics Dashboard';

// Set default time
// time can be overriden in the url using from/to parameteres, but this is
// handled automatically in grafana core during dashboard initialization
dashboard.time = {
  from: "now-6h",
  to: "now"
};


if(!_.isUndefined(ARGS.name)) {
  metrics = ARGS.name;
}


if( metrics.indexOf(",") == -1 ) {
    metricsArr = [ metrics ];
} else {
    metricsArr = metrics.split(",");
}


var seriesNamesArr = [];


for (var i = 0; i < metricsArr.length; i++) {
    seriesNamesArr.push(
        {
            'target': metricsArr[i]
        }
    )
}


dashboard.rows.push({
    title: 'Chart',
    height: '300px',
    panels: [
        {
            title: 'Metrics Chart',
            type: 'graph',
            span: 12,
            fill: 0,
            linewidth: 1,
            targets: seriesNamesArr,
//            targets: [
//
//                {
//                    'target': test_name
//                }
//            ],
            tooltip: {
                shared: true
            }
        }
    ]
});




return dashboard;
