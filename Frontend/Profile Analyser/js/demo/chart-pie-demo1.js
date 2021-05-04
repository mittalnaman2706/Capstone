// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx1 = document.getElementById("myPieChart1");

var script_tag = document.getElementById('piechart1')

var l  = script_tag.getAttribute("l");
var v  = script_tag.getAttribute("v");

var label = l.split("$")
var val = v.split("$")

var myPieChart1 = new Chart(ctx1, {
  type: 'doughnut',
  data: {
    labels: label,
    datasets: [{
      data: val,
      backgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#2085ec', '#8464a0', '#cea9bc', '#f1e59c', '#0dc7bb',
      '#aaf8e1', '#624634', '#c2b3b3'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#2085ec', '#8464a0', '#cea9bc', '#f1e59c', '#0dc7bb',
      '#aaf8e1', '#624634', '#c2b3b3'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: true,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
     legend: {
          display: true,
          position: 'bottom',
          labels: {
            fontColor: "#000080",
          }
        },
    cutoutPercentage: 0,
  },
});



