<template>
  <div class="scale-wrapper">
    <div class="scale-container">
      <div class="solid-color left-color" :style="{ width: leftWidth + '%' }"></div>
      <div class="scale-bar" :style="{ width: gradientWidth + '%' }"></div>
      <div class="solid-color right-color" :style="{ width: rightWidth + '%' }"></div>
    </div>
    <ul class="scale-values">
      <li v-for="value in scaleValues" :key="value" class="value">
        {{ value + unit }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HorizontalScale',
  props: {
    realMin: {
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
    realMax: {
      type: Number,
      required: true
    },
    unit: {
      type: String,
      default: ''
    }
  },
  computed: {
    leftWidth() {
      return ((this.min - this.realMin) / (this.realMax - this.realMin)) * 100;
    },
    gradientWidth() {
      return ((this.max - this.min) / (this.realMax - this.realMin)) * 100;
    },
    rightWidth() {
      return ((this.realMax - this.max) / (this.realMax - this.realMin)) * 100;
    },
    scaleValues() {
      const range = this.realMax - this.realMin;
      return [0, 25, 50, 75, 100].map(percent => {
        const label = this.realMin + (range * percent) / 100;
        return Math.round(label);
      });
    }
  }
}
</script>

<style>
.scale-wrapper {
  position: relative;
}

.scale-container {
  width: 100%;
  height: 20px;
  display: flex;
  border-radius: 5px;
  overflow: hidden;
}

.solid-color {
  height: 100%;
}

.left-color {
  background:hsl(240, 100%, 50%); /* Solid color for the left side */
}

.right-color {
  background: hsl(0, 100%, 50%); /* Solid color for the right side */
}

.scale-bar {
  height: 100%;
  background: linear-gradient(to right, hsl(240, 100%, 50%), hsl(120, 100%, 50%), hsl(0, 100%, 50%));
  transition: width 0.3s ease-in-out;
}

.scale-values {
  list-style: none;
  padding: 0;
  margin-top: 25px;
  display: flex;
  justify-content: space-between;
}

.value {
  position: relative;
  text-align: center;
}
</style>
