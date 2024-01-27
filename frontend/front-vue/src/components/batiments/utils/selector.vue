<template>
    <div class="grid-scoped">
      <h2>{{ currentFloor }}</h2>
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
          type: String,
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
          this.$emit('updateSelectedOption', event.target.value);
          this.selectedOption = event.target.value;
        }
      }
    };
  </script>
  
  <style scoped>
    .grid-scoped {
      align-items: center;
      gap: 2vh;
      margin: 0 2vw;
      padding: 0;
      display: flex;
      width: 67vw;
      justify-content: center;
      flex-direction: column;
    }

    select {
      padding: 10px 15px;
      font-size: 1rem;
      border: 2px solid var(--color-border);
      border-radius: 8px;
      background-color: var(--color-background);
      color: var(--color-text);
      outline: none;
      appearance: none;
      -webkit-appearance: none;
      -moz-appearance: none;
      background-image: url('data:image/svg+xml;utf8,<svg fill="%232c3e50" height="40" viewBox="0 0 24 24" width="40" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
      background-repeat: no-repeat;
      background-position: right 15px center;
      background-size: 20px; /* Increased icon size */
      cursor: pointer;
      transition: border-color 0.3s, box-shadow 0.3s;
    }

    select:hover {
      border-color: var(--color-border-hover);
    }

    select:focus {
      border-color: var(--color-inverted-border-hover);
      box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.2);
    }

    /* For browsers that do not support the 'appearance' property */
    select::-ms-expand {
      display: none;
    }

  </style>
  