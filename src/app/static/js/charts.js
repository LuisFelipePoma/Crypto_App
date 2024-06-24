const $ctx = document.getElementById('chart')
let myChart = null
export function plot_series (data) {
  if (myChart) myChart.destroy()
  // Clean canvas and
  // Sort data
  data = data.sort(function (a, b) {
    return a['timestamp'] - b['timestamp']
  })
	
  // unix timestamp to date (day-month-year)
  data = data.map(d => {
    const myUnixTimestamp = d['timestamp'] // start with a Unix timestamp
    const date = new Date(myUnixTimestamp * 1000) // convert timestamp to milliseconds and construct Date object

    d['timestamp'] = `${date.getDate()}-${
      date.getMonth() + 1
    }-${date.getFullYear()}` // get the day, month and year (note: month starts from 0)
    return d
  })

  const xlabels = data.map(d => d['timestamp'])
  const yvalues = data.map(d => d['close'])

  myChart = new Chart($ctx, {
    type: 'line',
    data: {
      labels: xlabels,
      datasets: [
        {
          label: 'Close',
          data: yvalues,
          borderWidth: 1
        }
      ]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  })
}
