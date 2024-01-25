<template>
	<div class="grid">
		<h2>Bat A</h2>
		<select :value="selectedOption" @change="updateSelectedOption">
			<option value="temperature">Température</option>
			<option value="humidity">Humidité</option>
			<option value="co2">CO2</option>
			<option value="activity">Présence</option>
		</select>
		<dataScale :min="valMin" :max="valMax" :real-min="realMin" :real-max="realMax" :unit="unit"></dataScale>
		<svg viewBox="0 0 877.99769 660">
			<g stroke="#000" stroke-opacity="0"
				stroke-width=".016258">
				<g v-for="(room, roomId) in roomData" :key="roomId" :id="roomId" :class="{ changeColor: true }"
					:style="{ fill: room.color }" @click="showRoomDetail(roomId)">
					<title>{{ roomId }}</title>
					<path v-for="(path, index) in room.path" :key="index" :id="'path' + roomId + '_' + index" :d="path" />
				</g>
			</g>
		</svg>
	</div>
	<RoomDetail v-if="roomName" :room="roomName" :key="roomName"></RoomDetail>
</template>
	
	
<script>
import { ref, reactive, onMounted, watch } from 'vue';
import dataScale from '../utils/dataScale.vue';
import RoomDetail from '@/components/roomDetail/roomDetail.vue';


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
      'hall-entrée-principale': { color: "grey", state: true, path: ["m 492.6509,417.31562 -185.3107,-0.0763 -20.65624,-18.58063 -2.287,-37.15 -37.03091,-4.18755 -13.39561,-13.39381 3.43858,-4.2612 -0.68028,-56.97856 -107.3343,-106.45387 -0.37356,-67.68611 17.02773,0.035 0.40023,53.56854 106.20946,0.14861 5.5e-4,42.41669 35.72518,0.30589 0.0609,25.44753 -31.89659,0.23215 -0.0364,8.56703 57.28644,60.07699 -27.2133,-0.61688 c -26.92054,0 -24.73779,35.65375 -0.16292,35.65375 l 206.26187,0.44619 z m -254.84973,-247.1034 -86.55646,0.22409 86.02429,83.17967 z"], data:{} },
      Bibliothèque: { color: "grey", state: true, path: ["m 659.89592,175.78247 v 29.29306 L 548.86098,205.49766 548.283,174.98256 424.06692,52.385503 C 505.18087,9.5276387 609.67197,-40.274795 776.63663,51.606699 Z"], data:{} },
      'hall-amphi': { color: "grey", state: true, path: ["m 492.79829,299.62691 18.55632,0.0184 -0.77739,-118.38551 -106.009,-110.075504 18.89599,-18.65265 124.8799,122.425624 0.83182,67.24113 111.08887,0.88489 -0.12762,-37.64153 39.99599,0.10614 0.18591,92.19436 h 18.45312 l -1.20597,142.44027 16.13137,66.03241 -27.0177,0.30249 c -1.39692,-42.58538 -35.42643,-96.92615 -102.22653,-98.69476 -57.37309,0.3798 -94.337,41.24086 -102.36188,81.79814 l -23.59281,-8.18048 14.23672,-64.00578 z"], data:{} },
      Patio: { color: "grey", state: true, path: ["m 549.2879,242.11086 -0.42336,-36.47815 111.11219,-0.208 0.25218,37.63295 z", "m 319.56539,334.56438 v -35.06252 l 173.11639,0.15769 0.0184,35.26009 z"], data:{} },
      amphi2: { color: "grey", state: true, path: ["m 476.66834,146.22263 -17.35213,18.7745 24.61594,26.18889 -0.37735,88.2229 27.22508,0.27549 0.32888,19.78334 -171.06945,0.0724 C 327.7133,242.49287 329.8476,186.90668 339.69264,139.03594 l 131.59941,1.60271 z"], data:{} },
      LocalElectrique: { color: "grey", state: true, path: ["m 488.23609,598.13111 -58.6398,-58.52789 48.8476,-58.10097 23.54145,8.36541 c -7.02323,31.6612 2.15388,60.60845 17.97735,82.87711 z"], data:{} },
      autocom: { color: "grey", state: true, path: ["m 470.10418,491.37048 -40.70877,47.98651 -29.09144,-29.07622 28.29784,-31.62266 z"], data:{} },
      Sanitaires: { color: "grey", state: true, path: ["m 426.20092,444.18412 2.41415,-26.63182 c 20.64908,0.0307 43.35596,-0.17302 64.0075,-0.0368 l -8.00353,36.1859 z", "m 478.44002,481.46488 -8.33498,9.82393 -41.45653,-12.68267 -5.39709,-27.07562 2.94373,-7.3248 58.42291,9.51831 z", "m 237.1962,253.46417 -85.79684,-82.96074 86.22493,0.001 z", "m 413.793,105.03785 -8.45684,-2.24469 -6.64067,9.08084 0.20862,16.29047 -29.21753,0.0822 0.0307,-32.861823 29.16421,-29.580823 34.07712,35.066876 -11.50941,-2.303281 z", "m 408.57765,129.15115 0.0693,10.70446 -16.64793,-0.20493 -0.006,-11.37117 6.9988,-0.0718 -0.25279,-16.32709 6.61177,-9.05489 8.44917,2.25837 7.64226,-6.468316 11.73894,2.415376 0.46018,17.62443 -8.48481,0.0123 z", "m 408.6695,139.85285 -0.0491,-10.68679 16.56442,-10.47235 8.48764,4.3e-4 0.15891,21.44108 z"], data:{} },
      amphi3: { color: "grey", state: true, path: ["m 867.22018,297.51519 -166.71181,0.0552 -0.23132,-98.73869 33.547,-32.6607 133.35269,-0.0804 z"], data:{} },
      Acceuil: { color: "grey", state: true, path: ["m 319.51336,299.49548 -0.0245,35.05958 -30.5467,-0.14297 c -27.9121,1.36047 -28.83933,-35.88194 -2.30065,-35.59147 z"], data:{} },
      ctaAmphi2: { color: "grey", state: true, path: ["m 297.29728,193.48004 -11.00235,-0.0368 0.12639,-18.62571 47.17752,1.08767 c -2.16535,26.0115 -4.09901,53.71812 0.58719,89.63405 l -52.85237,-0.34667 -24.44708,-25.77442 40.52587,0.0632 z"], data:{} },
      res: { color: "grey", state: true, path: ["m 256.69926,239.20327 0.0184,-8.18312 31.85331,-0.24052 -0.0706,-25.91628 -35.73082,-0.27426 v -11.01174 h 44.43106 l 0.043,45.75612 z"], data:{} },
      serv: { color: "grey", state: true, path: ["m 333.5994,175.72111 -47.16439,-1.06154 0.21045,-25.64471 51.13634,-0.23622 c -2.18744,10.61053 -2.73475,17.93907 -4.18222,26.94272 z"], data:{} },
      autres: { color: "grey", state: true, path: ["m 252.75032,174.79143 33.52191,0.0184 -0.11474,18.66964 -33.27323,0.0552 z", "m 113.67143,146.8951 0.0123,-38.12435 15.16806,-0.0491 0.0914,37.88273 z", "m 122.22453,183.82024 -27.599604,-27.52107 9.982784,-9.12195 24.37505,-0.42336 0.39023,29.64193 z", "m 369.59957,95.286624 0.0657,32.963126 -28.08016,-0.062 -16.00264,-19.02858 57.95604,-58.634348 15.16506,15.150209 z", "m 339.69387,139.01251 1.89537,-10.74815 50.36404,0.0307 0.0245,11.34823 z", "m 471.21542,140.56355 -37.32003,-0.3209 -0.58719,-39.05367 z", "m 484.0194,191.103 -24.54072,-26.11501 17.31624,-18.66547 25.38326,26.32823 z", "m 510.6757,279.23037 -26.69643,-0.13744 0.0368,-87.82696 18.17928,-18.57958 8.29602,8.68742 z"], data:{} },
      a001: { color: "grey", state: true, path: ["m 237.37008,339.69996 -3.47464,4.21462 -66.5775,-66.53241 31.77501,-31.84557 37.52686,37.37458 z"], data:{} },
      a002: { color: "grey", state: true, path: ["m 167.26094,277.28818 -34.35366,-34.31906 31.69905,-31.60119 34.47018,34.14566 z"], data:{} },
      a003: { color: "grey", state: true, path: ["M 132.86721,242.87046 98.410303,208.45298 129.39471,176.41334 164.557,211.33296 Z"], data:{} },
      a004: { color: "grey", state: true, path: ["M 98.342522,208.36733 70.635793,180.65501 94.966421,156.73842 122.21294,183.82496 Z", "M 70.577492,180.60869 25.37668,135.09572 44.618358,108.86284 94.941823,156.70455 Z", "m 113.51276,146.8654 -8.94663,0.25648 -9.956353,9.14035 -49.663159,-47.44823 68.560132,-0.0245 z"], data:{} },
      a005: { color: "grey", state: true, path: ["m 146.54221,162.23754 -0.0491,-53.22437 64.87889,0.23377 -0.17548,53.016 z"], data:{} },
      a006: { color: "grey", state: true, path: ["m 211.28833,162.1957 0.40495,-52.99049 41.16386,0.0724 -0.16627,52.91151 z"], data:{} },
      a007: { color: "grey", state: true, path: ["m 253.40745,109.19687 72.02073,0.21904 16.12358,18.84366 -3.7672,20.47778 -51.21972,0.21597 -0.27856,25.70239 -33.51866,0.0245 z"], data:{} },
      a008: { color: "grey", state: true, path: ["m 334.20677,265.60102 c 1.37121,10.89958 3.61491,23.83903 5.74529,33.86581 l -26.08348,-0.11535 -32.45527,-34.07615 z"], data:{} },
      a009: { color: "grey", state: true, path: ["m 400.25727,510.06399 c -31.67862,-29.87165 -61.92001,-62.09463 -92.9237,-92.66269 l 120.97079,0.0614 -2.12259,26.73104 -2.96452,7.33179 5.36487,27.08151 z"], data:{} },
      tour: { color: "grey", state: true, path: ["M 26.39348,113.141 A 12.823372,12.823372 0 0 1 13.570108,125.96437 12.823372,12.823372 0 0 1 0.7467369,113.141 12.823372,12.823372 0 0 1 13.570108,100.31763 12.823372,12.823372 0 0 1 26.39348,113.141 Z"], data:{} },
      amphi1: { color: "grey", state: true, path: ["M 706.05499,511.30807 A 102.73151,102.73151 0 0 1 603.32349,614.03958 102.73151,102.73151 0 0 1 500.59198,511.30807 102.73151,102.73151 0 0 1 603.32349,408.57657 102.73151,102.73151 0 0 1 706.05499,511.30807 Z"], data:{} },

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

.grid {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 50px;
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
</style>
	