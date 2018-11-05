console.log("working");
let rgbArray = ['rgb(255,99,71)', 'rgb(56,211,159)', 'rgb(255, 99, 132)', 'rgb(83,109,254)'];
let rgbArrayCount = 0;
var ctx = document.getElementById('myChart').getContext('2d');
let labels = document.getElementById("labels");
labels = convertToArray(labels);
let people = document.getElementById("values").getElementsByTagName("ul");
let arrayOfPeople = [];
for (let person of people) {
    let attrs = person.getElementsByTagName("li");
    let newPerson = {name: attrs[0].innerText, measures: convertToArray(attrs[1]), color: rgbArray[rgbArrayCount]};
    rgbArrayCount++;
    arrayOfPeople.push(newPerson);
}
function convertToArray(arrayInString) {
    let a = arrayInString.innerText;
    a = a.replace(/'/g, '"');
    return JSON.parse(a);
}

function getData(arrayOfPeople) {
    let data = [];
    for (let ind of arrayOfPeople) {
        let dataFull = {label: ind.name, backgroundColor: 'rgba(0, 0, 0, 0)', borderColor: ind.color, data: ind.measures};
        data.push(dataFull);
    }
    return data;
}
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: labels,
        datasets: getData(arrayOfPeople)
    },

    // Configuration options go here
    options: {}
});