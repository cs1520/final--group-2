const chartContext = document.getElementById("poke-interval-chart");
const name = '@' + document.getElementById("profile-name").textContent.split('@').splice(-1)[0].trim();
const startMonth = "Jan";
const endMonth = "Mar";

let chart = new window.Chart(chartContext, {
    type: "line",
    data: {
        datasets: [{
            label: "Pokes",
            data: [55, 162, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: "#00FFFF",
            borderColor: "#00FFFF",
            fill: false
        }],
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        label: "Pokes"
    },
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    min: startMonth,
                    max: endMonth
                }
            }]
        },
        title: {
            display: true,
            text: name + "'s 2021 Monthly Poke Totals"
        }
    }
});
