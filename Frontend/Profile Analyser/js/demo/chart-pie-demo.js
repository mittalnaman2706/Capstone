// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");

var script_tag = document.getElementById('piechart')

var partialac = script_tag.getAttribute("partialac");
var ac = script_tag.getAttribute("ac");
var wrong = script_tag.getAttribute("wrong");
var tle = script_tag.getAttribute("tle");
var runtimerr = script_tag.getAttribute("runtimerr");
var compilerr = script_tag.getAttribute("compilerr");


var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Partially Accepted", "Accepted", "Wrong", "TLE", "Runtime Error", "Compilation Error"],
    datasets: [{
      data: [partialac, ac, wrong, tle, runtimerr, compilerr],
      backgroundColor: ['#FFA500', '#366ecc', '#b9cc36', '#FFFF00', '#A52A2A', '#808080'],
      hoverBackgroundColor: ['#FFA500', '#366ecc', '#fb3155', '#FFFF00', '#A52A2A', '#808080'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
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
      display: false
    },
    cutoutPercentage: 0,
  },
});




