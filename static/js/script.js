// let data = [{'departures' : 'Chicago, IL','arrivals' : 'Milwaukee, WI'}]

d3.json('/citySelections').then(function(data) {
    // console.log(data)
    var departures = data.departures;
    var arrivals = data.arrivals;
    console.log(departures);
    console.log(arrivals);
  
    // *****Departures Dropdown*******
    for (let i = 0; i < departures.length; i++) {
      let options = d3.select("#selectDeparture");
      options.append("option").text(departures[i]).attr("value", departures[i]);
    }

    // *****Arrivals Dropdown*******
    for (let i = 0; i < arrivals.length; i++) {
        let options = d3.select("#selectArrival");
        options.append("option").text(arrivals[i]).attr("value", arrivals[i]);
    }
})

document.getElementById("searchTrips").addEventListener("click", findTrips);

function findTrips() {
    d3.json('/findTrips').then(function(data) {
        console.log(data)

        // let table = d3.select("#runsTable")
	    // let	tbody = table.append('tbody');

        // console.log(data[0])

        for (let i = 0; i < data.length; i++) {
            let run_id = data[i].run_id
            console.log(run_id)
            let departing = `${data[i].departure_location} on ${data[i].departure_date} at ${data[i].departure_time}`
            let arriving = `${data[i].arrival_location} on ${data[i].arrival_date} at ${data[i].arrival_time}`
            console.log(departing)

            // let run = tbody.append('tr')
            // run.append("td").text(run_id)
            // run.append("td").text(departing)
            // run.append("td").text(arriving)
          }

        // document.getElementById("runsTable").classList.toggle("hidden");
    })
}