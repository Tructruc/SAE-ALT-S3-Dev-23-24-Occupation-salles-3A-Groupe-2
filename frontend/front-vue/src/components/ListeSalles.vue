<template>
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

      <RoomDetail v-if="roomName" :room="roomName" :key="roomName" ></RoomDetail>
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
        // On garde seulement les données dont le capteur n'est pas déjà affiché.
        const dataUnique = Array.from(
          new Set(this.apiData.map(entry => JSON.stringify(entry)))
        ).map(entry => JSON.parse(entry));
  
        //return dataUnique.filter(entry => entry.room !== null);
        //On remplace les salles null par "Inconnue"
        return dataUnique.map(entry => {
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
        console.log("API config loaded:", this.apiBaseUrl);
      }).catch(error => {
        console.error("Error while loading API config:", error);
      });
    },
    methods: {
      async fetchApiData() {
        try {
          const response = await fetch(`${this.apiBaseUrl}/ByRoom/?depth=1`);
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
  </style>
  