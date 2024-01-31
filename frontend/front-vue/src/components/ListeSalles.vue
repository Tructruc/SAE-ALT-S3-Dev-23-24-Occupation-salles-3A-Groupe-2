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

      <RoomDetail v-show="roomName" :room="roomName" :key="roomName"></RoomDetail>
    </div>
</template>
  
<script>
import RoomDetail from "@/components/roomDetail/roomDetail.vue";
import loadApiConfig from '../utils/api.js';

  export default {
    name: 'ApiDataDisplay',
    components: {
      RoomDetail,
      apiBaseUrl: null,
    },
    data() {
      return {
        apiData: [],
        roomName: null,
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
    mounted() {
      loadApiConfig().then(apiIp => {
        this.apiBaseUrl = apiIp;
        this.fetchApiData();
      }).catch(error => {
        console.error("Error while loading API config:", error);
      });
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
  