<template>
  <div>
    <canvas id="lineChart"></canvas>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import Chart from 'chart.js/auto'
import 'chartjs-adapter-date-fns' // Import the adapter
import { fr } from 'date-fns/locale' // Import French locale

export default {
  extends: Line,
  props: {
    dates: { // array of Date objects
      type: Array,
      default: null
    },
    data: { // dictionary of data
      type: Object,
      default: null
    },
  },
  mounted () {


    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--color-text');
    const borderColor =getComputedStyle(document.documentElement).getPropertyValue('--color-border');


    const ctx = document.getElementById('lineChart').getContext('2d')
    const options = {
      type: 'line',
      data: {
        labels: this.dates,
        datasets: [{
          label: 'Temperature',
          data: this.data.temperature,
          borderColor: 'rgb(31,119,180)',
          backgroundColor: 'rgb(31,119,180)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Humidity',
          data: this.data.humidity,
          borderColor: 'rgb(255,127,14)',
          backgroundColor: 'rgb(255,127,14)',
          fill: false,
          tension: 0.1
        }, {
          label: 'CO2',
          data: this.data.co2,
          borderColor: 'rgb(44,160,44)',
          backgroundColor: 'rgb(44,160,44)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'Activity',
          data: this.data.activity,
          borderColor: 'rgb(214,39,40)',
          backgroundColor: 'rgb(214,39,40)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'TVOC',
          data: this.data.tvoc,
          backgroundColor: 'rgb(148,103,189)',
          borderColor: 'rgb(148,103,189)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'Illuminance',
          data: this.data.illuminance,
          borderColor: 'rgb(140,86,75)',
          backgroundColor: 'rgb(140,86,75)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'Infrared',
          data: this.data.infrared,
          borderColor: 'rgb(227,119,194)',
          backgroundColor: 'rgb(227,119,194)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'Infrared and visible',
          data: this.data.infrared_and_visible,
          borderColor: 'rgb(188,189,34)',
          backgroundColor: 'rgb(188,189,34)',
          fill: false,
          tension: 0.1,
          hidden: true
        }, {
          label: 'Pressure',
          data: this.data.pressure,
          borderColor: 'rgb(23,190,207)',
          backgroundColor: 'rgb(23,190,207)',
          fill: false,
          tension: 0.1,
          hidden: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'hour',
              displayFormats: {
                hour: 'HH:mm' // Format for hours
              }
            },
            adapters: {
              date: {
                locale: fr // Use French locale
              }
            },
            title: {
              display: true,
              text: 'Date',
              color: textColor
            },
            grid: {
              color: borderColor // Set grid line color to text color
            },
            ticks: {
              color: textColor
            }
          },
          y: {
            title: {
              display: true,
              text: 'value',
              color: textColor
            },
            grid: {
              color: borderColor,
            },
            ticks: {
              color: textColor
            }
          }
        },

        plugins: {
          tooltip: {
            titleFontColor: textColor, // set tooltip title color
            bodyFontColor: textColor // set tooltip body color
          },
          legend: {
            labels: {
              color: textColor // set legend text color
            }
          }
        }
      }
    }

    //log the datasets
    console.log(options.data.datasets[0])

    new Chart(ctx, options)


  }
}
</script>

<style scoped>
div{
  background-color: var(--color-background-mute);
  border-radius: 5px;
}

canvas {
  width: 100%;
  height: 50vh;
}
</style>