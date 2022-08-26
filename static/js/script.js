// let data = [{'departures' : 'Chicago, IL','arrivals' : 'Milwaukee, WI'}]

d3.json('/citySelections').then(function(data) {
    // console.log(data)
    var departures = data.departures;
    var arrivals = data.arrivals;
    console.log(departures)
    console.log(arrivals)
  
    // *****Departures Dropdown*******
    for (let i = 0; i < departures.length; i++) {
      let options = d3.select("#selectDeparture")
      options.append("option").text(departures[i]).attr("value", departures[i]);
    }

    // *****Arrivals Dropdown*******
    for (let i = 0; i < arrivals.length; i++) {
        let options = d3.select("#selectArrival")
        options.append("option").text(arrivals[i]).attr("value", arrivals[i]);
    }
})

// function findTrips() {
    d3.json('/findTrips').then(function(data) {
        console.log(data)
    })
// }