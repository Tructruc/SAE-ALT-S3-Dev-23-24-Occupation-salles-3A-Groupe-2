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
      console.log(days)

      // Calculate the date with the offset from now in minutes using thit format %Y-%m-%dT%H:%M:%S.%f %z
      let from = new Date(Date.now() - minutes * 60 * 1000).toISOString().slice(0, -5);

      let to = new Date(Date.now()).toISOString().slice(0, -5);

      await this.updateLine(from, to)
    },
    async updateLineFromTo(){
      let from = this.$refs.from.value;
      let to = this.$refs.to.value;

      // apply local offset to make it utc
      from = new Date(new Date(from) - new Date(Date.now()).getTimezoneOffset()).toISOString().slice(0,-5);
      to = new Date(new Date(to) - new Date(Date.now()).getTimezoneOffset()).toISOString().slice(0, -5);

      await this.updateLine(from, to)
    },
    async updateLine(from, to){
      this.loadedTimeLine = false
      this.visibleDatasets = this.getHiddenDatasetsFromTimeline();
      try {
        const sensor = await fetch('http://localhost:8000/ByRoom/'+this.room+'/?depth=1&from='+from+'&to='+to);
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
        console.log(days)

        // Calculate the date with the offset from now in minutes using thit format %Y-%m-%dT%H:%M:%S.%f %z
        let date = new Date(Date.now() - minutes * 60 * 1000).toISOString().slice(0, -5);

        const sensor = await fetch('http://localhost:8000/ByRoom/'+this.room+'/?depth=1&from='+date);
        const json = await sensor.json();


        const jsonLastDate = await fetch('http://localhost:8000/ByRoom/'+this.room+'/?depth=1&last_data=1');
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
    await this.loadData(60*24)
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
};
</script>

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



</style>