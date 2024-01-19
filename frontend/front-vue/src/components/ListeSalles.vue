<template>
    <div>
      <a
        v-for="(data, index) in filteredApiData"
        :key="index"
        :href="'#'+data.room+'_'+data.sensor.devicename"
        class="data-label"
      >
        <span class="field-name">Salle:</span> {{ data.room }}
        <br />
        <span class="field-name">Capteur:</span> {{ data.sensor.devicename }}
      </a>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ApiDataDisplay',
    data() {
      return {
        apiData: [],
      };
    },
    computed: {
      filteredApiData() {
        // On garde seulement les données qui ont une sall, et dont le capteur n'est pas déjà affiché.
        const dataUnique = Array.from(
          new Set(this.apiData.map(entry => JSON.stringify(entry)))
        ).map(entry => JSON.parse(entry));
  
        return dataUnique.filter(entry => entry.room !== null);
      },
    },
    mounted() {
      this.fetchApiData();
    },
    methods: {
      async fetchApiData() {
        try {
          const response = await fetch('http://localhost:8000/ByRoom/?format=json');
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
    background-color: #ffffff;
    color: gray;
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
  