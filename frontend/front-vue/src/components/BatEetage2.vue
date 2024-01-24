<template>
	<div class="grid">
		<h2>Etage 2</h2>
		<select :value="selectedOption" @change="updateSelectedOption">
			<option value="temperature">Température</option>
			<option value="humidity">Humidité</option>
			<option value="co2">CO2</option>
			<option value="activity">Présence</option>
		</select>
		<dataScale :min="valMin" :max="valMax" :real-min="realMin" :real-max="realMax" :unit="unit"></dataScale>
		<svg width="200%" height="30vw" viewBox="0 40 931.01 379">
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
			Tours: { color: "grey", state: true, path: ["m798.57 318.94c-0.30333-17.613 19.76-33.556 35.385-34.268 24.622 2.9271 36.347 11.803 37.122 30.908 1.6661 22.76-11.721 39.248-33.497 39.154-18.671-0.5652-40.719-11.356-39.01-35.794z", "m199.84 129.49c-0.30333-17.613 19.76-33.556 35.385-34.268 24.622 2.9271 36.347 11.803 37.122 30.908 1.6661 22.76-11.721 39.248-33.497 39.154-18.671-0.5652-40.719-11.356-39.01-35.794z"], data: {} },
			Autres: { color: "grey", state: true, path: ["m125.55 247.68 0.26238-34.08 135.95-1.51-0.1115-129.83 53.217 0.24727 1.1276 132.06 499.92-3.0441-1.1732-40.485 14.794-0.10146 3.3359 40.251 25.204-0.25472-0.74435 36.37-146.64 0.10388-0.20283 26.706-108.92 4.1456 0.1261-32.659z", "m253.97 273.7 0.70474-26.099 35.488-0.24189-0.77905 26.556z", "m829.92 170.78 52.612 0.19183-0.12781 18.298-23.719 21.269-25.452 0.42624z", "m315.21 82.568 35.9 0.3354 0.0934 36.088-21.268 2.8307 1.5149 92.206-15.13 0.0125z", "m224.58 165.92-50.929-0.35563-0.10296-31.366 24.41-0.069 3.8505 5.5585 59.24-0.2795 0.14835 45.338-24.769 0.13759z"], data: {} },
			San: { color: "grey", state: true, path: ["m202.67 139.43-4.0011-5.647-24.187 0.15903-0.3867-51.798 87.194-0.30773 0.0257 57.383z"], data: {} },
			E212: { color: "grey", state: true, path: ["m224.72 166.67 12.162 18.821 24.442 0.0499 0.17308 26.018-87.406 1.1708-0.13621-46.632z"], data: {} },
			E268: { color: "grey", state: true, path: ["m711.82 247.67 44.512 0.14425-3.3796 130.1-43.762-0.61912z"], data: {} },
			E267: { color: "grey", state: true, path: ["m757.03 247.89 61.733-0.11319-3.2887 130.49-62.736-0.48475z"], data: {} },
			E266: { color: "grey", state: true, path: ["m819.65 248.39 43.728-0.60269 14.643 10.93-2.5813 119.75-59.327-0.26069z"], data: {} },
			E211: { color: "grey", state: true, path: ["m126.09 213.11-0.35177-21.733-65.068 1.189-21.415-20.649 94.491-90.316 39.813 0.92667 0.14206 130.14z"], data: {} },
			E269: { color: "grey", state: true, path: ["m709.71 274.36-2.2966 102.54-67.621 0.56365-0.25197-100.24z"], data: {} },
			E270: { color: "grey", state: true, path: ["m602.16 278.69 36.914-1.0128 0.0772 99.414-37.264 1.2232z"], data: {} },
			E265: { color: "grey", state: true, path: ["m812.04 82.76 70.181-0.68999 0.08 88.845-66.989-0.42606z"], data: {} },
			E264: { color: "grey", state: true, path: ["m760.42 101.32 52.166 0.14268 3.5304 110.34-53.703 0.35422z"], data: {} },
			E263: { color: "grey", state: true, path: ["m698.84 103.35 60.392-1.6294 2.2249 110.71-59.097 0.43z"], data: {} },
			E262: { color: "grey", state: true, path: ["m606.02 212.62 5.9355-108.11 86.678-1.6685 3.4182 109.18z"], data: {} },
			E261: { color: "grey", state: true, path: ["m611.04 103.91-5.1121 108.97-84.17-0.0245 0.34435-106.65z"], data: {} },
			E260: { color: "grey", state: true, path: ["m457.13 106.96 64.28-0.224-0.11456 106.11-64.941 0.57153z", "m330.51 122.71 21.333-3.8363-0.086-35.395 105.25 0.71548-1.1106 128.87-124.14 1.2628z"], data: {} },
			E209: { color: "grey", state: true, path: ["m126 249.17 128.19-1.5688-0.73348 26.654 35.859 0.71878-2.2866 102.24-161-0.19009z"], data: {} },
			E208: { color: "grey", state: true, path: ["m290.52 246.91 168 0.0937-2.287 131.57-167.33-1.8113z"], data: {} },
			E210: { color: "grey", state: true, path: ["m1.3606 377.06-1.3606-169.98 37.873-34.58 22.076 20.341 64.716-0.68806-0.21638 184.35z"], data: {} },
			E207: { color: "grey", state: true, path: ["m458.69 246.31 142.56 0.49702 0.19728 132.33-143.67-1.0879z"], data: {} },
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
svg {
	border: dashed black 1px;
}

g {
	fill: rgb(183, 232, 247);
	stroke: rgb(0, 26, 255);
	fill-opacity: 1;
	stroke-width: 1px;
	stroke-linecap: round;
	stroke-linejoin: round;
	stroke-opacity: 1;
	transition: fill 1.2s, stroke 1s;
}

.grid {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 50px;
	width: 80vw;
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

/* Style de la liste déroulante */
select option {
	padding: 10px;
}

/* Style pour les options survolées */
select option:hover {
	background-color: #66afe9;
	color: #fff;
}

g.changeColor:hover {
	stroke-width: 4px;
	/* Augmenter la largeur du contour à 2 pixels */
}
</style>
	