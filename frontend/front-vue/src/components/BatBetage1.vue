<template>
	<div class="grid">
		<h2>Etage1</h2>
		<select :value="selectedOption" @change="updateSelectedOption">
			<option value="temperature">Température</option>
			<option value="humidity">Humidité</option>
			<option value="co2">CO2</option>
			<option value="activity">Présence</option>
		</select>
		<dataScale :min="valMin" :max="valMax" :real-min="realMin" :real-max="realMax" :unit="unit"></dataScale>
		<svg width="100%" height="100%" viewBox="0 0 877.99769 300">
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
			san: {
				color: "grey",
				state: true,
				path: [
					"m 411.34315,46.153649 c 23.72452,0.38611 47.78547,0.7777 72.02524,1.1722 l -3.79645,46.59951 -66.23478,-0.41214 z",
					"m 438.08215,46.588819 0.68176,47.08262",
					"m 434.6428,65.371529 15.91087,0.17637",
					"m 438.47767,73.903559 10.01972,0.0777 0.10225,-8.45502",
					"m 466.35913,47.049019 -1.11422,19.96551",
					"m 462.3095,67.014529 h 5.92589",
					"m 476.83327,66.795079 4.92512,0.2926",
					"m 412.14339,65.159969 3.85613,-0.0825",
					"m 421.74015,65.686059 6.85286,-0.03",
					"m 425.60586,65.686059 -0.24001,-19.3042"
				],
				data: {}
			},
			sousStation: {
				color: "grey",
				state: true,
				path: [
					"m 464.73646,183.70759 7.52828,0.0186 3.59238,-50.02195 -8.82476,-0.26083 z",
					"m 466.03859,155.20002 8.27356,0.017",
					"m 411.62583,133.55901 7.76162,-0.54805 1.06608,36.00524 -8.47319,0.64784 z"
				],
				data: {}
			},
			rgt: {
				color: "grey",
				state: true,
				path: ["m 370.1941,136.5927 41.43173,-3.03369 0.25583,26.05543 -39.28411,3.46335 z"],
				data: {}
			},
			couloir: {
				color: "grey",
				state: true,
				path: [
					"m 422.01693,221.81781 40.99971,-0.4579 4.01572,-87.9165 c 77.8224,5.91479 132.66954,1.68759 301.83145,47.92244 6.91445,16.3983 15.97422,17.42538 25.17783,17.42174 9.24991,-1.42047 18.49114,-1.65072 27.84514,-17.33542 1.88491,-9.16453 3.25357,-18.81819 -4.34172,-28.53588 -4.00288,-5.12143 -9.05938,-9.73686 -22.97551,-7.94556 -7.53772,0.97026 -13.14903,4.73027 -16.34498,10.95114 C 682.7389,125.54281 581.57546,113.63102 478.40519,108.24663 l 1.16675,-14.321271 -66.23478,-0.41214 0.40645,11.662951 c -98.54955,5.76522 -199.48262,16.5636 -313.38954,54.75829 -7.650273,-6.88175 -15.720033,-10.77785 -25.642503,-8.64105 -10.62867,2.28888 -16.73366,8.2785 -21.19727,17.64928 -4.2759,8.97671 -4.98113,16.88222 1.91812,27.56566 5.73238,8.87655 12.3846,13.0484 21.3185,13.21796 10.31193,0.19571 20.02395,-2.69571 27.817673,-11.98129 2.86055,-3.92184 5.02453,-7.93287 6.13121,-12.0793 70.88503,-23.79138 157.0172,-44.61068 308.68765,-52.65476 z"
				],
				data: {}
			},
			B101: {
				color: "grey",
				state: true,
				path: [
					"m 312.66082,113.32755 c 32.18625,-3.83968 65.89768,-6.54403 101.08279,-8.15138 l -3.85569,-93.585721 c -36.4258,1.38388 -72.23244,4.52013 -107.62361,8.83227 z"
				],
				data: {}
			},
			B102: {
				color: "grey",
				state: true,
				path: [
					"m 218.32871,128.54053 c 31.3953,-6.30443 62.8293,-11.62948 94.33211,-15.21298 L 302.26431,20.422719 c -36.15762,4.33875 -71.34911,10.6068 -106.0989,17.75691 z"
				],
				data: {}
			},
			B103: {
				color: "grey",
				state: true,
				path: ["m 102.25706,61.711469 c 30.83507,-8.68128 61.86762,-17.00902 93.90835,-23.53184 l 22.1633,90.360901 c -27.56145,5.62817 -55.18818,12.60391 -82.86466,20.60635 z"],
				data: {}
			},
			B104: {
				color: "grey",
				state: true,
				path: ["m 110.6998,185.66572 38.93726,-11.78931 25.96808,87.77854 c -28.4839,8.32013 -57.27527,18.60577 -86.203713,29.76767 l -21.91,-57.86595 9.25949,-23.83036 c 11.59527,0.11209 19.73724,-3.86389 26.067023,-9.9604 4.09567,-3.94473 6.08882,-8.99424 7.88186,-14.10019 z"],
				data: {}
			},
			B105: {
				color: "grey",
				state: true,
				path: ["m 149.63706,173.87641 c 30.00718,-8.32761 60.78703,-16.23808 95.08735,-22.24798 l 18.89053,88.1643 c -30.18975,6.08433 -59.56805,13.31294 -88.0098,21.86222 z"],
				data: {}
			},
			B106: {
				color: "grey",
				state: true,
				path: ["m 244.72441,151.62843 c 30.60334,-5.17445 61.55499,-9.71797 93.56699,-12.34079 l 12.34755,87.33653 c -33.10794,3.47902 -61.25307,8.06016 -87.02401,13.16856 z"],
				data: {}
			},
			B107: {
				color: "grey",
				state: true,
				path: ["m 560.0311,139.53609 c 31.09281,3.25157 62.03017,7.87022 92.83507,13.65361 l -20.55433,83.68832 c -27.38774,-4.61188 -54.9667,-8.93566 -83.83423,-11.31808 z"],
				data: {}
			},
			B108: {
				color: "grey",
				state: true,
				path: ["m 463.01664,221.35991 1.71982,-37.65232 7.52828,0.0186 3.59238,-50.02195 c 28.09423,0.9607 56.1545,2.84309 84.17398,5.83185 l -11.55349,86.02385 c -27.88071,-2.16645 -55.8284,-4.24822 -85.46097,-4.20003 z"],
				data: {}
			},
			B109: {
				color: "grey",
				state: true,
				path: ["m 478.40519,108.24663 c 23.94467,0.8006 48.29368,2.4467 72.83057,4.48569 l 10.99376,-98.300301 c -25.15533,-1.68229 -50.26828,-3.50216 -75.87947,-3.70448 z"],
				data: {}
			},
			B109b: {
				color: "grey",
				state: true,
				path: ["m 409.88792,11.590449 1.45523,34.5632 72.02524,1.1722 2.98166,-36.59831 c -26.05669,-0.5198 -51.43523,-0.0778 -76.46213,0.86291 z"],
				data: {}
			},
			B110: {
				color: "grey",
				state: true,
				path: ["m 562.22952,14.432019 c 24.87916,2.02615 49.77904,4.80547 74.70484,8.52737 l -18.79517,97.648831 c -22.15383,-3.06375 -44.3301,-6.06072 -66.90343,-7.8759 z"],
				data: {}
			},
			B111: {
				color: "grey",
				state: true,
				path: ["m 636.93436,22.959389 c 23.78467,3.4809 47.52549,7.92479 71.23458,13.06565 l -22.00171,96.810951 c -22.5281,-4.50991 -45.05729,-9.01661 -68.02804,-12.22777 z"],
				data: {}
			},
			B112: {
				color: "grey",
				state: true,
				path: ["m 716.57973,139.6648 21.94726,-96.505261 c 44.15216,10.74473 87.25011,25.37177 129.80476,41.99957 l -46.44497,96.293061 c 1.38366,-8.52305 3.1863,-17.14394 -3.26187,-27.00513 -4.80749,-7.35209 -11.56614,-9.79818 -19.13921,-9.75184 -12.40764,0.0759 -17.30672,5.22774 -21.26113,11.22667 z"],
				data: {}
			},
			B112b: {
				color: "grey",
				state: true,
				path: ["m 708.16894,36.025039 c 8.42179,1.8483 17.79734,3.99431 30.35805,7.1345 l -21.94726,96.505261 -30.4125,-6.82881 z"],
				data: {}
			},
			B113: {
				color: "grey",
				state: true,
				path: ["m 632.31184,236.87802 c 50.26601,8.91608 99.37561,22.17579 147.50106,39.13211 l 22.5564,-52.83704 -8.32766,-24.3855 c -6.15944,0.17634 -12.39466,-0.78649 -17.79224,-5.47083 -5.1901,-4.50428 -6.30797,-8.41398 -7.38559,-11.95091 -38.13395,-11.5108 -76.87,-20.62336 -115.99764,-28.17615 z"],
				data: {}
			},
			B115: {
				color: "grey",
				state: true,
				path: ["m 10.913257,91.932779 c 30.52017,-11.33811 60.96676,-21.38831 91.343803,-30.22131 l 33.20699,87.435411 -35.10998,10.78758 c -7.758963,-8.22241 -17.200533,-10.83196 -28.652613,-7.99645 -8.68038,2.14925 -14.8466,8.17383 -18.6313,18.11815 -1.73545,4.55989 -2.92285,9.33783 -3.70852,14.27814 z"],
				data: {}
			},
			B116a: {
				color: "grey",
				state: true,
				path: ["m 338.2914,139.28764 31.90296,-2.69496 3.26812,36.01632 -30.13441,2.30399 z"],
				data: {}
			},
			B116b: {
				color: "grey",
				state: true,
				path: [
					"m 350.63895,226.62417 c 23.44274,-2.41503 47.20563,-4.08629 71.37798,-4.80636 l -1.5634,-52.80161 -8.47319,0.64784 -0.0987,-10.0496 -39.28404,3.46335 0.86486,9.53121 -30.13441,2.30399 z",
					"m 411.98034,169.66404 0.51544,52.49465",
					"m 373.46248,172.609 38.51786,-2.94496"
				],
				data: {}
			}
			// Ajoutez le reste ici
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
	/* Aligner les éléments en colonne */
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
		