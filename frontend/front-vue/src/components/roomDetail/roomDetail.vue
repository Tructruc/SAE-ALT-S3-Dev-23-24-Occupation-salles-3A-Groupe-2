<template>
  <div ref="view" class="view">
    <h1 v-if="loaded">{{room}}</h1>
    <h2 v-if="loaded && lastDataReceived">Dernière donnée reçue : {{ lastDataReceived }}</h2>
    <h2 v-if="error_message">{{error_message}}</h2>
    <div class="dataContainer">
      <div class="topContainer">
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
    </div>

    <div class="bottomContainer">
      <div class="graphique">

        <TimeLine v-if=loadedTimeLine :data="timedDate" :dates="timeLabel" ref="timeLineComponent" :visible-datasets="visibleDatasets" />

      </div>

      <div id="sensorinfo">
        <DetailCapteur v-if=loaded :name="sensorName" :deveui="sensorDeveui" :building="sensorBuilding" :floor="sensorFloor" :externalPower="sensorExternalPower" />
      </div>
    </div><div class="timeSelector" v-if="loaded">

      <button v-on:click="updateLineMinutes(60)">1h</button>
      <button v-on:click="updateLineMinutes(6*60)">6h</button>
      <button v-on:click="updateLineMinutes(12*60)">12h</button>
      <button v-on:click="updateLineMinutes(24*60)">24h</button>
      <button v-on:click="updateLineMinutes(7*24*60)">7j</button>
      <p>De </p>
      <input ref="from" type="datetime-local">
      <p> à </p>
      <input ref="to" type="datetime-local">
      <button v-on:click="updateLineFromTo()">Valider</button>
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
import Gauge from "@/components/roomDetail/gauge.vue";
import Battery from "@/components/roomDetail/battery.vue";
import TimeLine from "@/components/roomDetail/TimeLine.vue";
import DetailCapteur from "@/components/roomDetail/DetailCapteur.vue";
import loadApiConfig from "@/utils/api.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

let sseClient;


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
    lastDataReceived: "",
    battery: 0,
    temp: 0,
    hum: 0,
    co2: 0,
    loaded: false,
    loadedTimeLine: false,
    error_message: "",
    chartData: null,
    visibleDatasets: null,
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
    duration: 60*24,
    from: null,
    to: null,

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
    

    },

    apiBaseUrl: null,
  }),
  methods:{
    getHiddenDatasetsFromTimeline() {
      if (this.$refs.timeLineComponent) {
        let ref = this.$refs.timeLineComponent;
        let hiddenTab = [];

        for (let i = 0; i < 9; i++) {
          hiddenTab.push(ref.chart.isDatasetVisible(i));
        }
        return hiddenTab;
      }
    },
    async updateLineMinutes(minutes){
      let days = minutes / 60 / 24;
      this.duration = minutes;

      // Calculate the date with the offset from now in minutes using thit format %Y-%m-%dT%H:%M:%S.%f %z
      let from = new Date(Date.now() - minutes * 60 * 1000).toISOString().slice(0, -5);

      let to = new Date(Date.now()).toISOString().slice(0, -5);

      await this.updateLine(from, to)
    },
    async updateLineFromTo(){
      let from = this.$refs.from.value;
      let to = this.$refs.to.value;
      this.duration = null;
      this.from = from;
      this.to = to;

      // apply local offset to make it utc
      from = new Date(new Date(from) - new Date(Date.now()).getTimezoneOffset()).toISOString().slice(0,-5);
      to = new Date(new Date(to) - new Date(Date.now()).getTimezoneOffset()).toISOString().slice(0, -5);

      await this.updateLine(from, to)
    },
    async updateLine(from, to){
      this.loadedTimeLine = false
      this.visibleDatasets = this.getHiddenDatasetsFromTimeline();
      try {
        const sensor = await fetch(`${this.apiBaseUrl}/ByRoom/`+this.room+'/?depth=1&from='+from+'&to='+to);
        const json = await sensor.json();

        if (json.all_data === undefined){
          this.error_message = "La salle « " + this.room + " » ne comporte pas de capteur"
          return;
        } else{
          //Clear old data
          this.timedDate.temperature = []
          this.timedDate.humidity = []
          this.timedDate.co2 = []
          this.timedDate.activity = []
          this.timedDate.tvoc = []
          this.timedDate.illuminance = []
          this.timedDate.infrared = []
          this.timedDate.infrared_and_visible = []
          this.timedDate.pressure = []
          this.timeLabel = []

          const view = this.$refs.view;
          const viewPosition = view.offsetTop;
          const offset = viewPosition + 80;
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

        this.loadedTimeLine = true
      } catch (e) {
        console.error(e)
      }
    },
    async loadData(minutes) {
      this.loaded = false;
      this.loadedTimeLine = false;
      this.visibleDatasets = this.getHiddenDatasetsFromTimeline();
      try {
        let days = minutes / 60 / 24;

        // Calculate the date with the offset from now in minutes using thit format %Y-%m-%dT%H:%M:%S.%f %z
        let date = new Date(Date.now() - minutes * 60 * 1000).toISOString().slice(0, -5);

        const sensor = await fetch(`${this.apiBaseUrl}/ByRoom/${this.room}/?depth=1&from=${date}`);
        const json = await sensor.json();


        const jsonLastDate = await fetch(`${this.apiBaseUrl}/ByRoom/${this.room}/?depth=1&last_data=1`);
        const jsonLastDateJson = await jsonLastDate.json();
        if (jsonLastDateJson.all_data && jsonLastDateJson.all_data.length > 0) {
          this.temp = jsonLastDateJson.all_data[jsonLastDateJson.all_data.length - 1].temperature;
          this.hum = jsonLastDateJson.all_data[jsonLastDateJson.all_data.length - 1].humidity;
          this.co2 = jsonLastDateJson.all_data[jsonLastDateJson.all_data.length - 1].co2;
          const lastData = jsonLastDateJson.all_data[jsonLastDateJson.all_data.length - 1];
          this.lastDataReceived = new Date(lastData.time).toLocaleString(undefined, {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          });
        }

        if (json.all_data === undefined){
          this.error_message = "La salle « " + this.room + " » ne comporte pas de capteur"
          return;
        } else{
          //Clear old data
          this.timedDate.temperature = []
          this.timedDate.humidity = []
          this.timedDate.co2 = []
          this.timedDate.activity = []
          this.timedDate.tvoc = []
          this.timedDate.illuminance = []
          this.timedDate.infrared = []
          this.timedDate.infrared_and_visible = []
          this.timedDate.pressure = []
          this.timeLabel = []

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

        this.battery = json.sensor.batterylevel;

        this.sensorName = json.sensor.devicename;
        this.sensorDeveui = json.sensor.deveui;
        this.sensorBuilding = json.building;
        this.sensorFloor = json.floor;
        this.sensorExternalPower = json.sensor.external_power;


        this.loaded = true;
        this.loadedTimeLine = true;
      } catch (e) {
        console.error(e)
      }
    }
  },
  async mounted () {
    try {
      const apiIp = await loadApiConfig();
      this.apiBaseUrl = apiIp;
      await this.loadData(this.duration);

      sseClient = this.$sse.create({
        url: `${this.apiBaseUrl}/Events/Data/${this.room}/`,
        format: 'json',
      })


      sseClient.on('error', (e) => {
        console.error('lost connection or failed to parse!', e);
      });

      sseClient.on('message', (message, lastEventId) => {
        this.temp = message.temperature;
        this.hum = message.humidity;
        this.co2 = message.co2;

        this.lastDataReceived = new Date(message.time).toLocaleString(undefined, {
          year: 'numeric',
          month: 'numeric',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });

        // If the graph is in "duration" mode, we add the new data to the graph
        if (this.duration) {
          this.updateLineMinutes(this.duration);
        }

      });

      sseClient.connect()
          .then(sse => {

            // Unsubscribes from event-less messages after 7 seconds
            setTimeout(() => {
              sseClient.off();
            }, 7000);

            // Unsubscribes from chat messages after 14 seconds
            setTimeout(() => {
              sseClient.off();
            }, 14000);
          })
          .catch((err) => {
            // When this error is caught, it means the initial connection to the
            // events server failed.  No automatic attempts to reconnect will be made.
            console.error('Failed to connect to server', err);
          });
    } catch (error) {
      console.error("Error while loading API config:", error);
    }
    
    // scroll to the top of this component
    const view = this.$refs.view;
    const viewPosition = view.offsetTop;
    const offset = viewPosition + 100;


    window.scrollTo({
      left: 0,
      top: viewPosition - 100 ,
      behavior: "smooth"
    });
  },
  beforeDestroy() {
    sseClient.disconnect();
  },

};
</script>

<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet"></link>

<style scoped>

.view
{
  display: flex;
  flex-direction: column;
  width: 67vw;
  justify-content: left;
}


.dataContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  row-gap: 1rem;
}

.topContainer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  column-gap: 1vw;
}

.bottomContainer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  column-gap: 1vw;
  width: 67vw;
  overflow: hidden;
}

.bottomContainer::-webkit-scrollbar {
  display: none;
}

.graphique {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  row-gap: 1vh;
  flex-grow: 1;
  height: 40vh;
}

#sensorinfo::-webkit-scrollbar {
  display: none;
}

#sensorinfo{
  height: 40vh;
  overflow: hidden;
}

h1 {
 font-weight: bold;
}

.timeSelector {
  display: flex;
  flex-direction: row;
  column-gap: 5px;
  width: 67vw;
  max-width: 67vw;
  flex-wrap: wrap;
  justify-content: left;
}


.timeSelector {
  background-color: var(--color-background-hover); /* Light grey background */
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: start;
  gap: 10px;
}

.timeSelector > button {
  padding: 10px 15px;
  background-color: var(--vt-c-black); /* Indigo shade */
  color: var(--vt-c-white); 
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 0.9rem;
  font-weight: 500;
}

.timeSelector > button:hover {
  /* Darken on hover */
  background-color: var(--vt-c-black-mute);
}

.timeSelector > input[type="datetime-local"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
}

.timeSelector > p {
  margin: 0; /* Remove default margins */
  color: #ffffff;
  font-size: 1rem;
}

input[type="datetime-local"] {
  font-family: 'Roboto', sans-serif; /* This applies the Roboto font */
  /* other styles */
}
</style>