<template>
	<div class="grid">
		<h2>Etage 1</h2>
		<select :value="selectedOption" @change="updateSelectedOption">
			<option value="temperature">Température</option>
			<option value="humidity">Humidité</option>
			<option value="co2">CO2</option>
			<option value="activity">Présence</option>
		</select>
		<dataScale :min="valMin" :max="valMax" :real-min="realMin" :real-max="realMax" :unit="unit"></dataScale>
		<svg width="100%" height="100%" viewBox="0 90 880 390">
			<g v-for="(room, roomId) in roomData" :key="roomId" :id="roomId" :class="{ changeColor: true }"
				:style="{ fill: room.color }" @click="showRoomDetail(roomId)">
				<title>{{ roomId }}</title>
				<path v-for="(path, index) in room.path" :key="index" :id="'path' + roomId + '_' + index" :d="path" />
			</g>
		</svg>
	</div>
	<RoomDetail v-if="roomName" :room="roomName" :key="roomName"></RoomDetail>
</template>
		
		
<script>
import { ref, reactive, onMounted, watch } from 'vue';
import dataScale from './dataScale.vue';
import RoomDetail from './roomDetail.vue';


export default {
	components: {
		RoomDetail,
		dataScale
	},

	setup() {

		const valMin = ref(0);
		const valMax = ref(500);
		const realMax = ref(500);
		const realMin = ref(0);
		const unit = ref("");

		const roomData = reactive({
      Autres: { color: "grey", state: true, path: ["M 200.96602,249.86911 5.9007839,249.50523 74.9936,176.86045 l 30.72025,0.0611 -0.0931,55.69863 94.29069,-0.33112 -0.15748,-55.17551 51.9988,-0.0818 -0.23047,43.29774 16.62386,-0.0845 -1.25177,88.40887 529.38299,-2.26938 -0.11038,21.97497 -579.14651,0.47977 z", "m 220.76042,377.00972 33.50628,0.15768 -0.4463,92.6294 -43.22862,0.0369 z m -3.34822,-47.46278 36.68808,-0.17387 0.25242,47.60303 -33.60593,-0.10044 z", "m 251.84328,176.99121 38.85182,0.2381 -0.60318,42.43195 -38.40852,0.53222 z"], data:{} },
      Tours: { color: "grey", state: true, path: ["M 270.63322,130.47864 A 33.973122,33.973122 0 0 1 236.6601,164.45176 33.973122,33.973122 0 0 1 202.68697,130.47864 33.973122,33.973122 0 0 1 236.6601,96.505516 33.973122,33.973122 0 0 1 270.63322,130.47864 Z", "m 868.78194,318.70521 a 34.231827,34.231827 0 0 1 -34.23183,34.23183 34.231827,34.231827 0 0 1 -34.23183,-34.23183 34.231827,34.231827 0 0 1 34.23183,-34.23182 34.231827,34.231827 0 0 1 34.23183,34.23182 z"], data:{} },
      Sanitaires: { color: "grey", state: true, path: ["m 105.73314,232.34519 0.0564,-55.42476 93.72306,0.0515 0.23196,55.08123 z"], data:{} },
      E100: { color: "grey", state: true, path: ["m 267.93042,220.26498 22.43882,-0.41443 0.55543,-42.63789 49.38786,-0.0393 -0.0607,131.04068 -73.12784,0.12828 z"], data:{} },
      E101: { color: "grey", state: true, path: ["m 340.56977,177.15478 170.54555,-0.0614 0.31336,130.36939 -171.06433,0.7478 z"], data:{} },
      E102: { color: "grey", state: true, path: ["m 511.48071,177.04468 157.81761,0.12621 0.0167,129.40627 -157.7641,0.86217 z"], data:{} },
      E103: { color: "grey", state: true, path: ["m 669.67236,177.18234 150.32728,0.0189 -0.0193,99.15921 -23.60646,29.59767 -126.58967,0.69396 z"], data:{} },
      E104: { color: "grey", state: true, path: ["m 651.46272,328.7921 144.8192,-0.0717 23.65283,31.97878 -0.0909,109.44822 -168.55264,-0.0611 z"], data:{} },
      E105: { color: "grey", state: true, path: ["m 493.18977,329.17425 157.61158,-0.12546 -0.0767,141.06159 -157.53257,-0.055 z"], data:{} },
      E106: { color: "grey", state: true, path: ["m 254.19532,329.05562 238.49403,0.1182 -0.0527,140.89553 -238.6947,-0.256 z"], data:{} },

    });

		const selectedOption = ref('activity');
		const roomName = ref(null);


		const updateSelectedOption = (event) => {
			selectedOption.value = event.target.value;
		};

		const showRoomDetail = (roomId) => {
			roomName.value = roomId;
		};

		const fetchAllRoomData = async () => {
			try {
				const response = await fetch('http://localhost:8000/ByRoom/?last_data=1&depth=1');
				const roomsData = await response.json();

				for (const roomKey in roomData) {
					if (roomData.hasOwnProperty(roomKey)) {
						const roomId = roomKey;
						const roomInfo = roomsData.find(room => room.room === roomId);

						if (roomInfo) {
							roomData[roomId].data = {
								id: roomInfo.all_data[0].id,
								time: roomInfo.all_data[0].time,
								temperature: roomInfo.all_data[0].temperature,
								humidity: roomInfo.all_data[0].humidity,
								activity: roomInfo.all_data[0].activity,
								co2: roomInfo.all_data[0].co2,
								tvoc: roomInfo.all_data[0].tvoc,
								illuminance: roomInfo.all_data[0].illuminance,
								infrared: roomInfo.all_data[0].infrared,
								infrared_and_visible: roomInfo.all_data[0].infrared_and_visible,
								pressure: roomInfo.all_data[0].pressure,
								state: true
							};
						} else {
							// Gérer le cas où les données de la salle ne sont pas disponibles
							roomData[roomId].state = false;
              console.log(roomId)
						}
					}
				}

				updateColors();
				updateScale();
			} catch (error) {
				console.error('Erreur lors de la récupération des données des salles.', error);
			}
		};

		const updateColors = () => {
			for (const roomId in roomData) {
				if (roomData.hasOwnProperty(roomId) && roomData[roomId].state) {
					const metricValue = parseFloat(roomData[roomId]['data'][selectedOption.value]);

					if (!isNaN(metricValue)) {
						roomData[roomId].color = getColorForMetric(metricValue, selectedOption.value);

					}

				}
			}
		};


		const getColorForMetric = (value, option) => {
			const getColor = (min, max, value) => {
				const normalizedValue = (value - min) / (max - min);
				const hue = (1 - normalizedValue) * 240; // Utilisez 120 pour des couleurs de bleu à rouge
				if (hue < 0) {
					return `hsl(0, 100%, 50%)`;
				}
				if (hue > 240) {
					return `hsl(240, 100%, 50%)`;
				}
				return `hsl(${hue}, 100%, 50%)`;
			};

			if (option === "temperature") {
				valMin.value = 14;
				valMax.value = 30;
				if (value > valMax.value) {
					realMax.value = value + 5;
				} else {
					realMax.value = 30;
				}
				if (value < valMin.value) {
					realMin.value = value - 5;
				} else {
					realMin.value = 14;
				}
				unit.value = "°C";
				return getColor(14, 30, value);
			}
			if (option == "humidity") {
				valMin.value = 40;
				valMax.value = 60;
				if (value > valMax.value) {
					realMax.value = value + 5;
				} else {
					realMax.value = 60;
				}

				if (value < valMin.value) {
					realMin.value = value - 5;
				} else {
					realMin.value = 40;
				}

				unit.value = "%";
				return getColor(40, 60, value);
			};
			if (option == "co2") {
				valMin.value = 0;
				valMax.value = 1500;
				if (value > valMax.value) {
					realMax.value = value + 5;
				} else {
					realMax.value = 1500;
				}
				if (value < valMin.value) {
					realMin.value = value - 5;
				} else {
					realMin.value = 0;
				}
				unit.value = "ppm";
				return getColor(0, 1500, value);
			};
			if (option == "activity") {
				valMin.value = 0;
				valMax.value = 500;
				if (value > valMax.value) {
					realMax.value = value + 5;
				} else {
					realMax.value = 500;
				}
				if (value < valMin.value) {
					realMin.value = value - 5;
				} else {
					realMin.value = 0;
				}
				unit.value = "";
				return getColor(0, 500, value);
			};
		};
		watch(
			() => selectedOption.value,
			() => {
				updateColors();
			}
		);


		onMounted(() => {
			fetchAllRoomData();
		});

		return { roomData, selectedOption, updateColors, updateSelectedOption, roomName, showRoomDetail, valMin, valMax, realMin, realMax, unit };
	}
};
</script>


<style scoped>
.grid {
  align-items: center;
  gap: 2vh;
}

/* Style de base pour le sélecteur */
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

/* Flèche personnalisée */
select::after {
  content: '\25BC';
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  pointer-events: none;
}

select option {
  padding: 10px;
}

select option:hover {
  background-color: #66afe9;
  color: #fff;
}

g {
  stroke: black;
  fill-opacity:1;
  stroke-width:1px;
  stroke-linecap:round;
  stroke-linejoin:round;
  stroke-opacity:1;

  transition: fill 1.2s, stroke 1s
}

g.changeColor:hover {
  filter: brightness(0.8);
}
</style>