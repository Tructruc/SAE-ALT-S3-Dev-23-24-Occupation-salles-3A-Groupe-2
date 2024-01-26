<template>
    <div class="grid-scoped">
      <h2>Etage {{ currentFloor === 0 ? 'RDC' : currentFloor }}</h2>
      <select :value="selectedOption" @change="updateSelectedOption">
        <option value="temperature">Température</option>
        <option value="humidity">Humidité</option>
        <option value="co2">CO2</option>
        <option value="activity">Présence</option>
      </select>
      <dataScale :min=min :max=max :real-min=realMin :real-max=realMax :unit=unit></dataScale>
    </div>
  </template>
  
  <script>
    import dataScale from './dataScale.vue';

    export default {
      components: {
        dataScale
      },
      name: 'Selector',
      props: {
        currentFloor: {
          type: Number,
          required: true
        },
        min: {
          type: Number,
          required: true
        },
        max: {
          type: Number,
          required: true
        },
        realMin: {
          type: Number,
          required: true
        },
        realMax: {
          type: Number,
          required: true
        },
        unit: {
          type: String,
          required: true
        }
      },
      data() {
        return {
          selectedOption: 'activity',
        };
      },
      methods: {
        updateSelectedOption(event) {
          this.selectedOption = event.target.value;
          // Mettre à jour les valeurs en fonction de l'option sélectionnée
        }
      }
    };
  </script>
  
  <style scoped>
    .grid-scoped {
      align-items: center;
      gap: 2vh;
      width: auto;
      margin: 0 2vw;
      padding: 0;
      display: flex;
      width: 67vw;
      justify-content: center;
      flex-direction: column;
    }

    select {
      padding: 10px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
      background-color: #fff;
      color: #333;
      outline: none;
      transition: border-color 0.3s;
    }
  </style>
  