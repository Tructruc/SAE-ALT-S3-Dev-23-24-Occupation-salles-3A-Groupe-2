<template>
	<div class="grid">
		<h2>RDC</h2>
		<select :value="selectedOption" @change="updateSelectedOption">
			<option value="temperature">Température</option>
			<option value="humidity">Humidité</option>
			<option value="co2">CO2</option>
			<option value="activity">Présence</option>
		</select>
		<dataScale :min="valMin" :max="valMax" :real-min="realMin" :real-max="realMax" :unit="unit"></dataScale>
		<svg width="100%" height="100%" viewBox="0 90 875 390">
			<g v-for="(room, roomId) in roomData" :key="roomId" :id="roomId" :class="{ changeColor: true }"
				:style="{ fill: room.color }" @click="showRoomDetail(roomId)">
				<title>{{ roomId }}</title>
				<path v-for="(path, index) in room.path" :key="index" :id="'path' + roomId + '_' + index" :d="path" />
			</g>
		</svg>
		<div class="det">
		
	</div>
	
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
			Autres: { color: "grey", state: true, path: ["m200.63 256.4-102.31 0.90161-93.899 1.9212 70.568-70.872 30.36-0.52343 1.3806 45.694 90.508 5.2796 1.3827-26.7 0.0884-26.554 52.708 0.0798c-8e-3 11.704 9e-3 23.409 0.0225 35.113l16.696-0.79525-1.1651 87.994-16.557 0.941 0.023 1.3221 541.63-4.7327 0.26695 30.303-571.5 7.8044z", "m222.99 412.76 28.645-4.1262 2.1854 61.163-43.139-0.24991zm-3.8216-68.04 29.575-0.78376 3.2099 63.572-29.209 4.8353z", "m251.86 185.28 41.846-0.49195-3.1296 32.463-38.893 2.9424z"], data: {} },
			Tours: { color: "grey", state: true, path: ["M798.57 318.94 C798.26724 301.326 818.33067 285.383 833.95565 284.671 858.57777 287.5981 870.30277 296.4731 871.07797 315.5781 872.74407 338.3381 859.35627 354.8261 837.58027 354.7321 818.90897 354.1669 796.86197 343.3761 798.57127 318.9381 Z", "M199.84 129.49 C199.5365 111.8764 219.6004 95.93338 235.22535 95.22145 259.84745 98.14856 271.57245 107.02356 272.34765 126.12856 274.01375 148.88856 260.62595 165.37656 238.84995 165.28256 220.17865 164.71736 198.13165 153.92656 199.84095 129.48856 Z"], data: {} },
			SAN: { color: "grey", state: true, path: ["M106.85 233 L106.2252 187.856 198.1552 185.8214 196.7053 238.2954 Z"], data: {} },
			E070: { color: "grey", state: true, path: ["m268.37 220.39 22.035-2.4212 3.4598-32.978 34.978 0.17673 2.1752 122.07-63.731 1.0782z"], data: {} },
			E001: { color: "grey", state: true, path: ["M329.48 184.77 L449.54 183.95163 L452.4076 306.36363 L331.7176 307.32209 Z"], data: {} },
			E002: { color: "grey", state: true, path: ["M450.96 182.83 L567.55 180.7207 L568.17316 305.5607 L453.60316 306.7191 Z"], data: {} },
			E003: { color: "grey", state: true, path: ["M569.09 180.62 L690.72 179.3506 L692.1943 303.9696 L567.4043 305.664 Z"], data: {} },
			E004: { color: "grey", state: true, path: ["M692.3 180.09 L814.31 178.7314 L819.6603 275.5614 L792.8333 303.2174 L692.9383 304.3751 Z"], data: {} },
			E005: { color: "grey", state: true, path: ["M696.06 338.68 L794.52 337.3425 L820.5926 368.5615 L811.077 465.7295 L695.9164 467.2701 Z"], data: {} },
			E006: { color: "grey", state: true, path: ["M573.06 339.83 L695.03 340.8219 L695.3374 469.1539 L576.7074 469.48989 Z"], data: {} },
			E007: { color: "grey", state: true, path: ["M392 341.52 L572.44 339.2837 L575.2276 467.2437 L394.3076 469.3713 Z"], data: {} },
			E008: { color: "grey", state: true, path: ["M255.11 469.7 L249.9662 344.6 L391.1962 341.4771 L394.0986 469.0071 Z"], data: {} },
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