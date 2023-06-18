$(document).ready(function() {
  $.ajax({
      url: "/api/trdata",
      type: "GET",
      success: function(response) {
          // Extract data from the API response
          var labels = response.labels;
          var datasets = response.datasets;

          labels = labels.reverse();
          datasets = datasets.reverse();

          // Prepare data for the chart
          var chartData = {
              labels: labels,
              datasets: datasets
          };

          // Create the line chart
          var ctx = document.getElementById('analytics').getContext('2d');
          var lineChart = new Chart(ctx, {
              type: 'line',
              data: chartData,
              options: {
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                    title : {
                      display: false,
                      text: 'Training Progression'
                    }
                  }
              }
          });
      },
      error: function(error) {
          console.log(error);
      }
  });
});
