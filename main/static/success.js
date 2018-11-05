console.log("working");
var ctx = document.getElementById('myChart').getContext('2d');
// let labs = document.getElementById("labels").getElementsByTagName("li");
let labels = document.getElementById("labels");
let measures = document.getElementById("measures");
labels = convertToArray(labels);
measures = convertToArray(measures);

function convertToArray(arrayInString) {
    let a = arrayInString.innerText;
    a = a.replace(/'/g, '"');
    return JSON.parse(a);
}

var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: labels,
        datasets: [{
            label: "My Progress",
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: 'rgb(255, 99, 132)',
            data: measures,
        }, {
            label: "My Progress",
            backgroundColor: "rgba(0, 0, 0, 0)",
            borderColor: "rgb(54, 162, 235, 1)",
            data: [62, 63, 63, 63],
        }]
    },

    // Configuration options go here
    options: {}
});