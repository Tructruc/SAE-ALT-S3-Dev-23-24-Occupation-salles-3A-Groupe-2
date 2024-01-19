<template>
  <div>
    <h3>{{valueName}}</h3>
    <canvas :id="uniqueid"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'GaugeChart',
  props: {
    value: {
      type: Number,
      required: true
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    valueName: {
      type: String,
      default: ''
    },
    unit: {
      type: String,
      default: ''
    },
    dangerValue: {
      type: Number,
      default: function() {
        try {
          return this.max;
        } catch (e) {
          return 100;
        }
      }
    }
  },
  computed: {
    textColor() {
      return getComputedStyle(document.documentElement).getPropertyValue('--color-text').trim();
    },
    backgroundColor() {
      return getComputedStyle(document.documentElement).getPropertyValue('--color-background-mute').trim();
    }
  },

  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      const centerTextPlugin = {
        id: 'centerText',
        afterDraw: (chart) => {
          let width = chart.width,
              height = chart.height,
              ctx = chart.ctx;

          ctx.restore();

          let text = `${this.value}${this.unit}`,
              fontSize = Math.min(100, width / text.length); // Dynamically set font size

          ctx.font = `${fontSize}px Arial`; // Use pixel size for more control
          ctx.fillStyle = this.textColor;
          ctx.textBaseline = 'middle';

          let textX = Math.round((width - ctx.measureText(text).width) / 2),
              textY = height / 2 + height / 15;

          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      };



      // Determine if the value exceeds the danger value
      const isDanger = this.value > this.dangerValue;

      const cappedValue = Math.max(Math.min(this.value, this.max), this.min);
      const adjustedValue = cappedValue - this.min
      const adjustedEmpty = this.value > this.dangerValue ? 0 : this.dangerValue-this.min -adjustedValue;
      const adjustedDanger = this.value > this.dangerValue ? this.max - this.min - adjustedValue : this.max - this.dangerValue;

      const data = {
        labels: ["Value", "Empty", "Empty danger"],
        datasets: [{
          data: [adjustedValue, adjustedEmpty, adjustedDanger],
          backgroundColor: [isDanger ? "Red" : "Green", "lightgrey", "lightCoral"],
          borderColor: this.backgroundColor
        }]
      };

      const options = {
        type: 'doughnut',
        data: data,
        options: {
          rotation: 225, // Start angle in degrees
          circumference: 270, // Sweep angle in degrees
          cutout: '80%', // Inner cutout percentage
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              enabled: false // Disable tooltips
            }
          }
        },
        plugins: [centerTextPlugin]
      };

      const ctx = document.getElementById(this.uniqueid).getContext('2d');
      new Chart(ctx, options);
    }
  },
  watch: {
    value() {
      this.createChart();
    },
    min() {
      this.createChart();
    },
    max() {
      this.createChart();
    }
  },
  data() {
    return {
      uniqueid: 'gauge-chart-' + crypto.randomUUID()
    };
  }
};
</script>


<style scoped>
div {
  width: 300px;
  padding: 10px;
  background-color: var(--color-background-mute);
}

h3 {
  text-align: center;
  margin: 0;
  padding: 0;
}
</style>
