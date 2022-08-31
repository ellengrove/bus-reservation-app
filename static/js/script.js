

d3.json('/citySelections').then(function(data) {

    var departures = data.departures;
    var arrivals = data.arrivals;
  
    // *****Departures Dropdown*******
    let depOptions = d3.select("#selectDeparture");
    depOptions.append("option").text("View all").attr("value", "all")
    for (let i = 0; i < departures.length; i++) {
      depOptions.append("option").text(departures[i]).attr("value", departures[i]);
    }

    // *****Arrivals Dropdown*******
    let arrOptions = d3.select("#selectArrival");
    arrOptions.append("option").text("View all").attr("value", "all")
    for (let i = 0; i < arrivals.length; i++) {
        arrOptions.append("option").text(arrivals[i]).attr("value", arrivals[i]);
    }
})

document.getElementById("searchTrips").addEventListener("click", findTrips);

function findTrips() {
    // Store value of dropdown menu selections to use for API call
    let arrivalSel = d3.select("#selectArrival").node().value.split(',')
    let departSel = d3.select("#selectDeparture").node().value.split(',')
    // console.log(arrivalSel)


    let table = d3.select("#runsTable")
    // Clear page of previous run history
    d3.select("#unavailRun").text("")
    d3.select("#runsHeader").remove()
    d3.select("#runsBody").remove()

    // Call API based on departure and arrival selections
    d3.json(`/find/${departSel[0]}/${arrivalSel[0]}`).then(function(data) {
    // d3.json(`/findTrips/${departSel[0]}/${arrivalSel[0]}`).then(function(data) {
        // If API returns empty results, return error message
        if (data.length === 0) {
            d3.select("#unavailRun").text("We're sorry. No routes found.")
        } else {
        // If API returns non-empty results, iterate through
            let thead = table.append('thead').attr("class","table-light").attr("id","runsHeader");
            let header = thead.append("tr")
            header.append("td").text('Run Number')
            header.append("td").text("Departing From")
            header.append("td").text("Arriving In")

        for (let i = 0; i < data.length; i++) {
            let run_id = data[i].run_id
            let departing = `${data[i].departure_location} on ${data[i].departure_date} at ${data[i].departure_time}`
            let arriving = `${data[i].arrival_location} on ${data[i].arrival_date} at ${data[i].arrival_time}`


            let	tbody = table.append('tbody').attr("id","runsBody");
            let run = tbody.append('tr')
            run.append("td").text(run_id)
            run.append("td").text(departing)
            run.append("td").text(arriving)
            console.log(run_id)
            console.log(arriving)
            console.log(departing)
          }
        }
    })
}