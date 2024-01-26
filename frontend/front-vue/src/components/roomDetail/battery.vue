<template>
  <div>
    <h3>Battery</h3>
    <canvas id="myChart"></canvas>
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
    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--color-text').trim();

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
              display: false
            },
            ticks: {
              color: textColor
            }
          },
          y: {
            stacked: true,
            grid: {
              display: false
            },
            beginAtZero: true, // Ensures the y-axis starts at zero
            max: 100, // Optionally, set the maximum value of y-axis,
            ticks: {
              color: textColor
            }
          }
        }
      }
    });
  }
};
</script>

<style scoped>

div {
  width: 16vw;
  max-height: 32vh;
  padding: 1rem;
  background-color: var(--color-background-mute);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
h3 {
  margin: 0;
  padding: 0;
}

</style>
