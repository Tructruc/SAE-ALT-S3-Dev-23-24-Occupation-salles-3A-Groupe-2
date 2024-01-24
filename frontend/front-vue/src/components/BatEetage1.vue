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
			autres: { color: "grey", state: true, path: ["m200.63 256.4-102.31 0.90161-93.899 1.9212 70.568-70.872 30.36-0.52343 1.3806 45.694 90.508 5.2796 1.3827-26.7 0.0884-26.554 52.708 0.0798c-8e-3 11.704 9e-3 23.409 0.0225 35.113l16.696-0.79525-1.1651 87.994-16.557 0.941 0.023 1.3221 541.63-4.7327 0.26695 30.303-571.5 7.8044z", "m222.99 412.76 28.645-4.1262 2.1854 61.163-43.139-0.24991zm-3.8216-68.04 29.575-0.78376 3.2099 63.572-29.209 4.8353z", "m251.86 185.28 41.846-0.49195-3.1296 32.463-38.893 2.9424z"], data: {} },
			Tours: { color: "grey", state: true, path: ["m798.57 318.94c-0.30333-17.613 19.76-33.556 35.385-34.268 24.622 2.9271 36.347 11.803 37.122 30.908 1.6661 22.76-11.721 39.248-33.497 39.154-18.671-0.5652-40.719-11.356-39.01-35.794z", "m199.84 129.49c-0.30333-17.613 19.76-33.556 35.385-34.268 24.622 2.9271 36.347 11.803 37.122 30.908 1.6661 22.76-11.721 39.248-33.497 39.154-18.671-0.5652-40.719-11.356-39.01-35.794z"], data: {} },
			SAN: { color: "grey", state: true, path: ["m106.85 233-0.6248-45.143 91.93-2.0346-1.4499 52.473z"], data: {} },
			E100: { color: "grey", state: true, path: ["m268.37 220.39 22.035-2.4212 3.4598-32.978 34.978 0.17673 2.1752 122.07-63.731 1.0782z"], data: {} },
			E101: { color: "grey", state: true, path: ["m329.48 184.77 185.8-0.46592 2.8676 122.41-186.43 0.60501z"], data: {} },
			E102: { color: "grey", state: true, path: ["m516.78 184.51 152.73-3.3911 1.1203 123.55-152.48 1.6944z"], data: {} },
			E103: { color: "grey", state: true, path: ["m670.74 180.44 143.57-1.712 5.3503 96.83-26.827 27.656-121.46 1.5112z"], data: {} },
			E104: { color: "grey", state: true, path: ["m665.66 339.74 128.86-2.3978 26.072 31.219-9.5156 97.168-145.56 2.6009z"], data: {} },
			E105: { color: "grey", state: true, path: ["m482.93 341.6 180.64-1.6988 0.30746 128.33-180.48 0.33602z"], data: {} },
			E106: { color: "grey", state: true, path: ["m255.11 469.7-5.1438-125.1 232.06-3.1229-0.2786 127.12z"], data: {} },
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