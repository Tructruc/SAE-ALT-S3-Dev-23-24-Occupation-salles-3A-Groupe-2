<template>
  <div ref="view">
    <h1 v-if="loaded">{{room}}</h1>
    <h2 v-if="error_message">{{error_message}}</h2>
    <div class="grid">
      <div id="battery">
        <battery v-if=loaded :battery=battery />
      </div>

      <div id="Temperature">
        <gauge v-if=loaded :value=temp :min=-20 :max=50 :value-name='"Temperature"' :unit="'°C'" :danger-value=35 />
      </div>

      <div id="Humidity">
        <gauge v-if=loaded :value=hum :min=0 :max=100 :value-name='"Humidity"' :unit="'%'" :danger-value=80 />
      </div>

      <div id="CO2">
        <gauge v-if=loaded :value=co2 :min=0 :max=3000 :value-name='"CO2"' :unit="'ppm'" :danger-value=1500 />
      </div>

      <div class="graphique">
        <TimeLine v-if=loaded :data="timedDate" :dates="timeLabel" />
      </div>

      <div id="sensorinfo">
        <DetailCapteur v-if=loaded :name="sensorName" :deveui="sensorDeveui" :building="sensorBuilding" :floor="sensorFloor" :externalPower="sensorExternalPower" />
      </div>

    </div>
  </div>
</template>

<script>
import {Scatter} from 'vue-chartjs'
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
import Battery from "@/components/battery.vue";
import TimeLine from "@/components/TimeLine.vue";
import DetailCapteur from "@/components/DetailCapteur.vue";

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
    DetailCapteur,
    TimeLine,
    Battery,
    Gauge,
    Scatter
  },
  props: {
    room: {
      type: String,
      required: true
    }
  },

  data: () => ({
    battery: 0,
    temp: 0,
    hum: 0,
    co2: 0,
    loaded: false,
    error_message: "",
    chartData: null,
    timedDate: {
      temperature: [],
      humidity: [],
      co2: [],
      activity: [],
      tvoc: [],
      illuminance: [],
      infrared: [],
      infrared_and_visible: [],
      pressure: [],
    },
    timeLabel: [],

    sensorName: '',
    sensorDeveui: '',
    sensorBuilding: '',
    sensorFloor: '',
    sensorExternalPower: false,

    chartOptions: {
      type: "line",
      x: {
        type: 'time',
        time: {
          // Luxon format string
          tooltipFormat: 'DD t'
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
      // ... other chart options if needed
    },
  }),
  async mounted () {
    this.loaded = false

    try {
      const sensor = await fetch('http://localhost:8000/ByRoom/'+this.room+'/?depth=1');
      const json = await sensor.json();

      if (json.all_data === undefined){
        this.error_message = "La salle « " + this.room + " » ne comporte pas de capteur"
        return;
      } else{
        const view = this.$refs.view;
        const viewPosition = view.offsetTop;
        const offset = viewPosition + 80;

        window.scrollBy({
          top: 1000,
          behavior: "smooth"
        });
      }



      for (const [key, value] of Object.entries(json.all_data)) {
        let utcTime = new Date(value.time);

        let time = new Date(utcTime.getTime() - utcTime.getTimezoneOffset() * 60 * 1000);
        if (!this.timeLabel.includes(time)) {
          this.timeLabel.push(time)
        }
        // add the values to the correct array
        this.timedDate.temperature.push(value.temperature)
        this.timedDate.humidity.push(value.humidity)
        this.timedDate.co2.push(value.co2)
        this.timedDate.activity.push(value.activity)
        this.timedDate.tvoc.push(value.tvoc)
        this.timedDate.illuminance.push(value.illuminance)
        this.timedDate.infrared.push(value.infrared)
        this.timedDate.infrared_and_visible.push(value.infrared_and_visible)
        this.timedDate.pressure.push(value.pressure)
      }

      this.battery = json.sensor.batterylevel

      this.temp = json.all_data[json.all_data.length - 1].temperature
      this.hum = json.all_data[json.all_data.length - 1].humidity
      this.co2 = json.all_data[json.all_data.length - 1].co2

      this.sensorName = json.sensor.devicename;
      this.sensorDeveui = json.sensor.deveui;
      this.sensorBuilding = json.building;
      this.sensorFloor = json.floor;
      this.sensorExternalPower = json.sensor.external_power;


      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  },
};
</script>

<style scoped>

.grid {
  display: grid;
  gap: 10px;
  width: 64vw;
  grid-template-columns: 16vw 16vw 16vw 16vw;
  grid-template-rows: auto 50vh;

}

#battery {
  grid-column: 1;
  grid-row: 1;
}

#Temperature {
  grid-column: 2;
  grid-row: 1;
}

#Humidity {
  grid-column: 3;
  grid-row: 1;
}

#CO2 {
  grid-column: 4;
  grid-row: 1;
}

#sensorinfo {
  grid-column: 4;
  grid-row:  2;
}

.graphique {
  grid-column: 1 / span 3;
  grid-row: 2;
  height: 50vh;
}


h1 {
 font-weight: bold;
}


</style>