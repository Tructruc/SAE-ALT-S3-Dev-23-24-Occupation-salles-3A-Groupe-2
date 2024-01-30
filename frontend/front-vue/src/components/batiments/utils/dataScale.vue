<template>
  <div class="wrapper">
    <div class="scale-wrapper">
      <div class="scale-container">
        <div class="solid-color left-color" :style="{ width: leftWidth + '%' }"></div>
        <div class="scale-bar" :class="battery ? 'battery-color' : 'normal-color'" :style="{ width: gradientWidth + '%' }"></div>
        <div class="solid-color right-color" :style="{ width: rightWidth + '%' }"></div>
      </div>
      <ul class="scale-values">
        <li v-for="value in scaleValues" :key="value" class="value">
          {{ value + unit }}
        </li>
      </ul>
    </div>
  <div class="empty-room">
    <div class="empty-room__color"/>
    <div class="empty-room__title">No Data</div>
  </div></div>
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
    },
    battery: {
      type: Boolean,
      default: false
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
  width: 35vw;
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
  transition: width 0.3s ease-in-out;
}
.normal-color {
  background: linear-gradient(to right, hsl(240, 100%, 50%), hsl(120, 100%, 50%), hsl(0, 100%, 50%));
}

.battery-color {
  background: linear-gradient(to right,  hsl(0, 100%, 50%), hsl(120, 100%, 50%));
}

.scale-values {
  list-style: none;
  padding: 0;
  margin-top: 5px;
  display: flex;
  justify-content: space-between;
}

.value {
  position: relative;
  text-align: center;
}

.empty-room{
  margin-left: 1vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.empty-room__color {
  width: 1vw;
  height: 1vw;
  background: grey;
  border-radius: 5px;
}

.wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
</style>
