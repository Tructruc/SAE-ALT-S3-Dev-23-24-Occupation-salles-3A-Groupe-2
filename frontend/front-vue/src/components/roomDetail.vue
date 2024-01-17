<template>
  <div>
    <h1>{{room}}</h1>
    <gauge :value=37 :min=-20 :max=50 :value-name='"Temperature"' :unit="'°C'" :danger-value=35></gauge>
    <gauge :value=52 :min=0 :max=100 :value-name='"Humidity"' :unit="'%'" :danger-value=80></gauge>
    <Line v-if="loaded" :data="chartData"  :options="chartOptions" width="500" height="400" style="background-color: white"></Line>
  </div>
</template>

<script>
import {Line} from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import Gauge from "@/components/gauge.vue";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)



export default {
  components: {
    Gauge,
    Line
  },

  data: () => ({
    loaded: false,
    chartData: null,
    chartOptions: {
      scales: {
        x: {
          ticks: {
            // Custom tick configuration
            callback: function(val, index) {
              // Show label only for every 5th data point
              return index % 3 === 0 ? this.getLabelForValue(val) : '';
            },
          },
        },
        // ... other scale configurations if needed
      },
      // ... other chart options if needed
    },
  }),
  async mounted () {
    this.loaded = false

    try {
      const sensor = await fetch('http://localhost:8000/Sensor/24e124128c016684/?depth=1');
      const json = await sensor.json();

      this.room = json.room

      var tempdata = {
        labels: [],
        datasets: []

      }

      /*
      example json:
      {
    "deveui": "24e124128c016684",
    "devicename": "AM107-14",
    "room": "B106",
    "building": "B",
    "floor": 1,
    "batterylevel": 7.87,
    "externalpowersource": false,
    "all_data": [
        {
            "id": 81,
            "time": "2024-01-10T16:55:15.243039+01:00",
            "temperature": 21.8,
            "humidity": 38.0,
            "activity": 134.0,
            "co2": 1691.0,
            "tvoc": 273.0,
            "illuminance": 31.0,
            "infrared": 4.0,
            "infrared_and_visible": 23.0,
            "pressure": 994.1
        },
       */

      const datasetTemplates= {
        temperature: { label: 'Temperature', backgroundColor: 'red' },
        humidity: { label: 'Humidity', backgroundColor: 'blue' },
        activity: { label: 'Activity', backgroundColor: 'green', hidden: true },
        co2: { label: 'CO2', backgroundColor: 'orange', hidden: true },
        tvoc: { label: 'TVOC', backgroundColor: 'purple', hidden: true },
        illuminance: { label: 'Illuminance', backgroundColor: 'yellow', hidden: true },
        infrared: { label: 'Infrared', backgroundColor: 'black', hidden: true },
        infrared_and_visible: { label: 'Infrared and visible', backgroundColor: 'brown', hidden: true },
        pressure: { label: 'Pressure', backgroundColor: 'pink', hidden: true },
      }

      for (const [key, value] of Object.entries(datasetTemplates)) {
        tempdata.datasets.push({
          label: value.label,
          backgroundColor: value.backgroundColor,
          data: [],
          hidden: value.hidden
        })
      }

      for (const [key, value] of Object.entries(json.all_data)) {
        let time = new Date(value.time)
        let timeformated = time.toLocaleString("fr-FR", {timeZone: "Europe/Paris", year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'});

        tempdata.labels.push(timeformated)
        for (const [key2, value2] of Object.entries(datasetTemplates)) {
          tempdata.datasets.find(x => x.label === value2.label).data.push(value[key2])
        }
      }



      this.chartData = tempdata

      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  },
};
</script>
