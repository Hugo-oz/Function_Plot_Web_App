<template>
  <div class="container">
    <h1 class="title">Function Plotter</h1>
    <div class="input-container">
      <label for="functionInput">Enter a function: y(x) = </label>
      <input v-model="functionText" id="functionInput" type="text" />
    </div>
    <div class="input-container">
      <label for="rangeStart">Start X:</label>
      <input v-model="rangeStart" id="rangeStart" type="number" />
      <label for="rangeEnd">End X:</label>
      <input v-model="rangeEnd" id="rangeEnd" type="number" />
    </div>
    <button @click="plotFunction" class="plot-button">Plot</button>
    <div class="canvas-container">
      <canvas ref="plotCanvas" class="plot-canvas"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      functionText: '',
      rangeStart: -10,
      rangeEnd: 10,
    };
  },
  methods: {
    async plotFunction() {
      try {
        const response = await axios.post('http://localhost:8000/plot', {
          functionText: this.functionText,
          rangeStart: this.rangeStart,
          rangeEnd: this.rangeEnd,
        });

        const data = response.data;
        const points = Array.isArray(data) ? data : [];

        const canvas = this.$refs.plotCanvas;
        const ctx = canvas.getContext('2d');
        const canvasWidth = canvas.width;
        const canvasHeight = canvas.height;

        ctx.clearRect(0, 0, canvasWidth, canvasHeight);

        ctx.strokeStyle = 'blue';
        ctx.beginPath();
        for (const point of points) {
          const x = this.calculateXPosition(point.x, points);
          const y = this.calculateYPosition(point.y, points);
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      } catch (error) {
        console.error('Error plotting the function:', error);
      }
    },
    calculateXPosition(x, points) {
      const canvas = this.$refs.plotCanvas;
      const min = Math.min(...points.map((point) => point.x));
      const max = Math.max(...points.map((point) => point.x));
      const range = max - min;
      const adjustedX = (x - min) / range;
      return adjustedX * (canvas.width - 20) + 10;
    },
    calculateYPosition(y, points) {
      const canvas = this.$refs.plotCanvas;
      const min = Math.min(...points.map((point) => point.y));
      const max = Math.max(...points.map((point) => point.y));
      const range = max - min;
      const adjustedY = (y - min) / range; 
      return (canvas.height - 20) - adjustedY * (canvas.height - 20) + 10; 
    },
  },
};
</script>

<style>
.container {
  text-align: center;
}

.title {
  font-size: 48px;
  margin-bottom: 40px;
}

.input-container {
  margin-bottom: 10px;
}

.plot-button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.plot-canvas {
  border: 1px solid #000000;
  margin-top: 20px;
  width: 800px;
  height: 600px;
}
</style>