const metadata = document.getElementById("user-metadata");

const canvas_pokesReceived = document.getElementById("user-pokes-received");
const canvas_pokesBy = document.getElementById("user-pokes-by");
const canvas_pokesBetween = document.getElementById("user-pokes-between");

const userId = metadata.getAttribute("data-user-id");
const sessionUserId = metadata.getAttribute("data-session-user-id");


async function loadPokesReceivedData() {
    const pokesReceivedRequest = await fetch("/api/pokes?id=" + encodeURIComponent(userId))
    const pokesReceivedData = await pokesReceivedRequest.json();
    return pokesReceivedData;
}

async function loadPokesByData() {
    const pokesByRequest = await fetch("/api/pokesby?id=" + encodeURIComponent(userId));
    const pokesByData = await pokesByRequest.json();
    return pokesByData;
}

async function loadPokesBetweenData() {
    const pokesBetweenRequest = await fetch("/api/pokesbetween?id=" + encodeURIComponent(userId));
    const pokesBetweenData = await pokesBetweenRequest.json();
    return pokesBetweenData;
}

// Mon: ...
// Sun: ...
// labels = [..., Sun, Mon]

/*
day = null
pokes = 0
data = []
for poke in pokes:
  cur_day = poke.date.substr(3)
  pokes++
  if cur_day != day:
	labels = [cur_day, ...labels]
	data = [pokes, ...data]

pokesReceived.forEach(poke => pokers.add(poke.pokee); pokeTimes.add(poke.time))
datasets: pokers, pokeTimes

data = {Mon: 0, ...}
forEach:
	data[date.substring(3)]++
*/

const DAYS_OF_WEEK = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function getWeekdayLabels() {
	// day = index of current day of week
	const day = new Date().getDay();

	// order labels from current day (in reverse)
	// i.e. on Tuesday, labels = [..., Sat, Sun, Mon, Tue]
	let labels = [];
	for (let i = day + 7; i > day; i--) {
		labels = [DAYS_OF_WEEK[i % 7], ...labels];
	}

	return labels;
}

async function loadCharts() {
	// get label order for weekday charts
	const weekdayLabels = getWeekdayLabels();

    // the data of the pokes received by a user
    const pokesReceivedData = await loadPokesReceivedData();
    const pokesReceivedDays = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0};
    pokesReceivedData.forEach((poke) => pokesReceivedDays[poke.created.substring(0, 3)]++);

	new window.Chart(canvas_pokesReceived, {
		type: "line",
		data: {
			datasets: [{
				label: "Pokes",
				// map the poke data in order of the labels index array
				data: weekdayLabels.map((key) => pokesReceivedDays[key]),
				backgroundColor: "#00FFFF",
				borderColor: "#00FFFF",
				fill: false
			}],
			labels: weekdayLabels,
			label: "Pokes received"
		},
		options: {
			scales: {
				xAxes: [{
					ticks: {
						min: weekdayLabels[0],
						max: weekdayLabels[6]
					}
				}]
			},
			title: {
				display: true,
				text: userId + "'s Poke Totals This Week"
			}
		}
	});

    // load the statistics for a logged in user looking at their own page
    if (sessionUserId && sessionUserId === userId) {
        // the data of the pokes sent by a user
        const pokesByData = await loadPokesByData();
        const pokesByDays = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0};
        pokesByData.forEach((poke) => pokesByDays[poke.created.substring(0, 3)]++);
        new window.Chart(canvas_pokesBy, {
            type: "line",
            data: {
                datasets: [{
                    label: "Pokes",
                    // map the poke data in order of the labels index array
                    data: weekdayLabels.map((key) => pokesByDays[key]),
                    backgroundColor: "#00FFFF",
                    borderColor: "#00FFFF",
                    fill: false
                }],
                labels: weekdayLabels,
                label: "Pokes You Have Sent This Week"
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            min: weekdayLabels[0],
                            max: weekdayLabels[6]
                        }
                    }]
                },
                title: {
                    display: true,
                    text: userId + "'s Poke Totals This Week"
                }
            }
        });
    } 
    
    // load the statistics for a logged-in user looking at another user's page
    else if (sessionUserId) {
        // the data of the pokes given from one user to another
        const pokesBetweenData = await loadPokesBetweenData();
        const pokesBetweenDays = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0};
        pokesBetweenData.forEach((poke) => pokesBetweenDays[poke.created.substring(0, 3)]++);
        new window.Chart(canvas_pokesBetween, {
            type: "line",
            data: {
                datasets: [{
                    label: "Pokes",
                    // map the poke data in order of the labels index array
                    data: weekdayLabels.map((key) => pokesBetweenDays[key]),
                    backgroundColor: "#00FFFF",
                    borderColor: "#00FFFF",
                    fill: false
                }],
                labels: weekdayLabels,
                label: "Pokes you have sent to " + userId
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            min: weekdayLabels[0],
                            max: weekdayLabels[6]
                        }
                    }]
                },
                title: {
                    display: true,
                    text: "How Often You Have Poked " + userId + " This Week"
                }
            }
        });
    }
}

loadCharts();
