var ctx = document.getElementById('analytics');
var chart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
              datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
    async function getData() {
        const apiUrl = "@api/data"

        const response = await fetch(apiUrl)
        const lineChartData = await response.json()

        HTMLFormControlsCollection.log(lineChartData)
    }

    getData()