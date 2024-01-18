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


    const ctx = document.getElementById('lineChart').getContext('2d')
    const options = {
      type: 'line',
      data: {
        labels: this.dates,
        datasets: [{
          label: 'Temperature',
          data: this.data.temperature,
          borderColor: 'red',
          backgroundColor: 'rgba(255, 0, 0, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Humidity',
          data: this.data.humidity,
          borderColor: 'blue',
          backgroundColor: 'rgba(0, 0, 255, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'CO2',
          data: this.data.co2,
          borderColor: 'green',
          backgroundColor: 'rgba(0, 255, 0, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Activity',
          data: this.data.activity,
          borderColor: 'orange',
          backgroundColor: 'rgba(255, 165, 0, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'TVOC',
          data: this.data.tvoc,
          borderColor: 'yellow',
          backgroundColor: 'rgba(255, 255, 0, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Illuminance',
          data: this.data.illuminance,
          borderColor: 'purple',
          backgroundColor: 'rgba(128, 0, 128, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Infrared',
          data: this.data.infrared,
          borderColor: 'brown',
          backgroundColor: 'rgba(165, 42, 42, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Infrared and visible',
          data: this.data.infrared_and_visible,
          borderColor: 'pink',
          backgroundColor: 'rgba(255, 192, 203, 0.5)',
          fill: false,
          tension: 0.1
        }, {
          label: 'Pressure',
          data: this.data.pressure,
          borderColor: 'black',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          fill: false,
          tension: 0.1
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
              text: 'Date'
            }
          },
          y: {
            title: {
              display: true,
              text: 'value'
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
