<template>
  <div id="battery">
    <h3>Battery</h3>
    <div class="chart-container" style="position: relative;">
      <canvas id="myChart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'Battery',
  props: {
    battery: {
      type: Number,
      required: true
    }
  },
  mounted() {

    const batteryIsLow = this.battery < 20;

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [''],
        datasets: [{
          label: '',
          data: [this.battery],
          backgroundColor: batteryIsLow ? "red" : 'green'
        }, {
          label: '',
          data: [100 - this.battery],
          backgroundColor: 'lightgrey'
        }]
      },
      options: {
        aspectRatio: 1,
        plugins: {
          legend: {
            display: false // Hides the legend
          },
          tooltip: {
            enabled: false // Hides the tooltips
          },
        },
        scales: {
          x: {
            stacked: true,
            grid: {
              display: true // Optionally, hide the grid lines for x-axis
            }
          },
          y: {
            stacked: true,
            grid: {
              display: false // Optionally, hide the grid lines for y-axis
            },
            beginAtZero: true, // Ensures the y-axis starts at zero
            max: 100 // Optionally, set the maximum value of y-axis
          }
        }
      }
    });
  }
};
</script>

<style scoped>
#battery {
  padding: 10px;
  width: 300px;
  background-color: white;
  color: black;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

h3 {
  margin: 0;
  padding: 0;
}

canvas {
  height: 300px;
}

</style>
