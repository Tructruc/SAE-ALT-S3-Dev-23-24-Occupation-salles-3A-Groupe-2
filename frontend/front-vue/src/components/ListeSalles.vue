<template>
    <div class="title-container">
      <h1>Liste des salles disponnibles</h1>
    </div>
    
    <div>
      <div
        v-for="(data, index) in filteredApiData"
        :key="index"
        class="data-label"
        @click="roomName = data.room"
      >
        <span class="field-name">Salle:</span> {{ data.room }}
        <br />
        <span class="field-name">Capteur:</span> {{ data.sensor.devicename }}
      </div>

      <RoomDetail v-if="roomName" :room="roomName" :key="roomName"></RoomDetail>
    </div>
</template>
  
<script>
import RoomDetail from "@/components/roomDetail/roomDetail.vue";
import loadApiConfig from '../utils/api.js';
import api from "../utils/api.js";

  export default {
    name: 'ApiDataDisplay',
    components: {
      RoomDetail,
    },
    data() {
      return {
        apiData: [],
        roomName: null,
        sse: null,
        apiBaseUrl: null,
      };
    },
    computed: {
      filteredApiData() {
        const uniqueData = {};
        this.apiData.forEach(entry => {
          const uniqueKey = `${entry.room}-${entry.sensor.devicename}`; // Exemple de clé unique
          uniqueData[uniqueKey] = entry;
        });
        return Object.values(uniqueData).map(entry => {
          if (entry.room === null) {
            entry.room = "Inconnue";
          }
          return entry;
        });
      },
    },
    async mounted() {
      this.apiBaseUrl = await loadApiConfig()

      this.sse = this.$sse.create({
        url: `${this.apiBaseUrl}/Events/Sensor/`,
        format: 'json',
      })

      this.sse.on('error', (e) => {
        console.error('lost connection or failed to parse!', e);
      });

      this.sse.on('message', (message, lastEventId) => {
        const uniqueKey = `${message.room}-${message.devicename}`;
        const existingEntry = this.apiData.find(entry => {
          return `${entry.room}-${entry.sensor.devicename}` === uniqueKey;
        });

        if (existingEntry) {
        } else {
          this.apiData.push({
            room: message.room,
            sensor: {
              devicename: message.devicename,
            },
          });
        }

      });
      this.sse.connect()
          .then(sse => {

            // Unsubscribes from event-less messages after 7 seconds
            setTimeout(() => {
              this.sse.off();
            }, 7000);

            // Unsubscribes from chat messages after 14 seconds
            setTimeout(() => {
              this.sse.off();
            }, 14000);
          })
          .catch((err) => {
            // When this error is caught, it means the initial connection to the
            // events server failed.  No automatic attempts to reconnect will be made.
            console.error('Failed to connect to server', err);
          });
      await this.fetchApiData();
    },
    methods: {
      async fetchApiData() {
        try {
          const response = await fetch(`${this.apiBaseUrl}/ByRoom/?depth=1&last_data=0`);
          const jsonData = await response.json();
          this.apiData = jsonData;
        } catch (error) {
          console.error('Error fetching API :', error);
        }
      },
    },
    beforeDestroy() {
      this.sse.disconnect();
      this.sse.off();
    }
  };
</script>
  
<style scoped>
  .data-label {
    margin: 5px;
    padding: 10px;
    background-color: var(--color-background-mute);
    color: var(--color-text);
    border-radius: 5px;
    text-decoration: none;
    display: inline-block;
    transition: background-color 0.3s, color 0.3s;
    user-select: none;
  }
  
  .data-label:hover {
    background-color: #3498db;
    color: white;
  }
  
  .field-name {
    font-weight: bold;
  }

  .title-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }
  </style>
  