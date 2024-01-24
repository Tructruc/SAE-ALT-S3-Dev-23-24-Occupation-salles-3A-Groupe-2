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
    visibleDatasets: { // array of booleans
      type: Array,
      default: [true, true, false, false, false, false, false, false, false]
    }
  },
  data: () => ({
    chart: null
  }),
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
          tension: 0.1,
          hidden: !this.visibleDatasets[0]
        }, {
          label: 'Humidity',
          data: this.data.humidity,
          borderColor: 'rgb(255,127,14)',
          backgroundColor: 'rgb(255,127,14)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[1]
        }, {
          label: 'CO2',
          data: this.data.co2,
          borderColor: 'rgb(44,160,44)',
          backgroundColor: 'rgb(44,160,44)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[2]
        }, {
          label: 'Activity',
          data: this.data.activity,
          borderColor: 'rgb(214,39,40)',
          backgroundColor: 'rgb(214,39,40)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[3]
        }, {
          label: 'TVOC',
          data: this.data.tvoc,
          backgroundColor: 'rgb(148,103,189)',
          borderColor: 'rgb(148,103,189)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[4]
        }, {
          label: 'Illuminance',
          data: this.data.illuminance,
          borderColor: 'rgb(140,86,75)',
          backgroundColor: 'rgb(140,86,75)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[5]
        }, {
          label: 'Infrared',
          data: this.data.infrared,
          borderColor: 'rgb(227,119,194)',
          backgroundColor: 'rgb(227,119,194)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[6]
        }, {
          label: 'Infrared and visible',
          data: this.data.infrared_and_visible,
          borderColor: 'rgb(188,189,34)',
          backgroundColor: 'rgb(188,189,34)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[7]
        }, {
          label: 'Pressure',
          data: this.data.pressure,
          borderColor: 'rgb(23,190,207)',
          backgroundColor: 'rgb(23,190,207)',
          fill: false,
          tension: 0.1,
          hidden: !this.visibleDatasets[8]
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
                hour: 'dd/MM HH:mm' // Format for hours
              },
              tooltipFormat: 'dd/MM/yyyy HH:mm', // Format for tooltip
            },
            adapters: {
              date: {
                locale: fr // Use French locale
              }
            },
            title: {
              display: false,
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
              display: false,
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

    this.chart = new Chart(ctx, options)


  }
}
</script>

<style scoped>
div{
  background-color: var(--color-background-mute);
  border-radius: 5px;
  width: 50vw;
  height:100%;
}

</style>