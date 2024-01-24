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
			<g transform="matrix(0 -6.1357 6.1357 0 -508.28 1358.5)" stroke="#000" stroke-opacity="0"
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
			Bibliotheque: { color: "grey", state: true, path: ["m192.76 190.39h-4.7742l-0.0139-18.009 5.0752-0.13451 19.855-20.216c6.985 13.22 15.071 30.174 0.0961 57.386z"], data: {} },
			'hall-entrée-principale': { color: "grey", state: true, path: ["m 153.53877,162.20853 -0.0187,-29.29947 3.0003,-3.3448 6.0164,-0.36965 0.67946,-5.9893 2.1345,-2.1876 0.71465,0.58503 9.337,0.0383 17.231,-17.515 11.031,-0.0477 1e-5,2.7302 -8.7371,0.43445 v 16.891 L 188,124.09106 l -0.0133,5.889 -4.32,-0.0644 0.0874,-5.2286 -1.372,-0.0339 -9.7582,9.2864 0.11106,-4.4754 -5.8057,-0.1904 -0.0277,32.60537 m 26.61834,-39.96542 0.0196,-14.323 -13.506,13.985 z"], data: {} },
			'hall-amphi': { color: "grey", state: true, path: ["m 166.85366,161.97196 -0.0103,1.26874 5.6574,-0.0386 0.0397,3.0048 19.361,-0.23218 18.037,-17.215 2.9621,3.0172 -19.953,20.353 -10.96,0.16183 -0.14615,18.369 5.9836,-0.0341 1e-5,6.2723 h -14.889 v 3.0075 l -23.215,-0.19655 -10.762,2.6291 -0.0493,-4.2243 c 6.5807,-0.2423 15.396,-3.9649 16.413,-16.84 -0.0124,-9.1274 -7.4313,-15.077 -13.768,-16.373 l 1.4923,-4.1003 10.473,2.2786 v -0.76364"], data: {} },
			amphi2: { color: "grey", state: true, path: ["m197.54 160.51-3.0222-2.8106-4.2232 3.9314-14.297-0.0644-0.0122-3.6036-0.15938 8.1242-3.2243 0.0536-0.0118-27.881c9.2976-2.0089 18.275-1.6085 26.077-4e-3l-0.20947 21.247z"], data: {} },
			amphi1: { color: "grey", state: true, path: ["m122.6 188.02c-6.4591-14.245 7.864-28.713 22.603-21.679 6.8326 3.0533 10.756 10.285 9.7217 17.736-4.0191 18.74-26.367 17.082-32.325 3.9425z"], data: {} },
			tgbt: { color: "grey", state: true, path: ["m124.07 162.68 9.4231-9.8213c1.857 2.4023 6.673 6.1186 9.4336 7.9797l-1.4258 4.0246c-5.8064-1.0879-9.1873-0.26083-13.505 2.4349z"], data: {} },
			autocom: { color: "grey", state: true, path: ["m141.26 159.49c-2.5552-2.2259-5.8252-3.9919-7.6534-6.7422l4.8431-4.4544 4.8914 4.3889z"], data: {} },
			SAN: {
				color: "grey", state: true, path: ["m149.03 152.3 4.407 0.37807c-5e-3 3.3654-0.0461 6.8842-0.0683 10.25l-5.8301-1.2692z",
					"m142.94 160.61-1.6321-1.0257 2.1217-6.8317 4.3955-0.82867 1.119 0.37399-1.506 9.31z",
					"m180.18 121.35 13.376-13.792-0.11562 14.1z",
					"m204.29 150.28 0.36584-1.3783-1.48-1.0823-2.7439 0.2322 0.0714-4.9911 5.3599 0.0357 4.8211 4.7532-5.6911 5.532 0.35127-1.8539z",
					"m200.36 149.43h-1.7553v-2.6668l1.7188-0.0126 0.0632 1.3437 2.787-0.20897 1.45 1.1327-0.38337 1.2162 1.0379 1.257-0.36627 1.9645-2.819-0.0442-0.036-1.2749z",
					"m198.62 149.47 1.6944-0.0369 1.7136 2.6921-0.0213 1.3512-3.4625 0.0379z"], data: {}
			},
			Amphi3: { color: "grey", state: true, path: ["m173.16 224.19-0.0284-27.12 15.895 0.0569 5.3147 5.3147-0.2217 21.666z"], data: {} },
			Accueil: { color: "grey", state: true, path: ["m172.51 134.75-5.4168 0.0317 0.019-4.8498c-0.0439-4.5074 5.403-4.7201 5.4294-0.37035z"], data: {} },
			ctaAmphi2: { color: "grey", state: true, path: ["m189.95 131.39-0.0369-1.8906 2.9702 0.0253-0.19907 7.6642c-1.3607-0.0579-8.4986-0.65422-14.514-0.0754l0.018-8.4218 4.0065-3.8654-0.0821 6.5989z"], data: {} },
			res: { color: "grey", state: true, path: ["m182.24 124.59 1.4264 0.0283v5.2432h4.3228l0.0758-5.8259h1.7947v7.2414l-7.6633 0.0884z"], data: {} },
			serv: { color: "grey", state: true, path: ["m192.77 137.21 0.19647-7.9284 4.0557 0.41082 0.13466 8.1249z"], data: {} },
			autres: {
				color: "grey", state: true, path: ["m193.3 124.06-0.38629 5.4189-2.9972-0.0796-0.0499-5.4027z",
					"m197.54 101.46 6.0424-0.0894 0.10716 2.4692-6.0915-0.0115z",
					"m191.45 102.76 4.4854-4.4982 1.4867 1.627 0.0998 4.0293-4.8942-0.0352z",
					"m205.91 142.98-5.2925 2e-5v-4.5503l3.3571-2.8416 9.4191 9.0558-2.5374 3.235z",
					"m198.77 138.25 1.7351 0.27823-0.16886 8.18-1.7336 0.016z",
					"m198.5 159.64 0.0523-6.0837 6.36-0.0538z",
					"m190.28 161.72 4.2321-3.8738 2.9463 2.6776-4.2563 4.0933z",
					"m175.9 166.07 0.0224-4.351 14.185 2e-5 2.9226 2.9156-1.1634 1.2082z",], data: {}
			},
			A001: { color: "grey", state: true, path: ["m166.12 121.38c-0.0112-0.0291-0.9304-0.73429-0.6787-0.57859l10.406-10.849 5.5333 5.437-6.0805 6.0148z"], data: {} },
			A002: { color: "grey", state: true, path: ["m176.01 109.89 5.3789-5.6782 5.5148 5.5148-5.4574 5.6047z"], data: {} },
			A003: { color: "grey", state: true, path: ["m181.46 104.13 5.7505-5.4397 5.3749 5.2258-5.5975 5.7738z"], data: {} },
			A004: { color: "grey", state: true, path: ["m187.26 98.69 4.5898-4.4586 3.9287 4.0428-4.3484 4.4637z", "m191.85 94.231 6.5946-6.5722 5.1899 2.005 0.0321 0.4479-7.8289 8.1656z", "m197.54 101.44-0.0321-1.5686-1.5856-1.6644 7.7523-8.0418 0.0191 9.7615-3.4111 0.0176-0.0386 0.0951 3.4191 0.0401 9e-3 1.1931z"], data: {} },
			A005: { color: "grey", state: true, path: ["m195 107.18 8.6421-0.46432-0.0381 10.574-8.6869-0.24278z"], data: {} },
			A006: { color: "grey", state: true, path: ["m195.01 117.15 8.5933 0.21129-0.24769 6.832-8.3233 0.0767z"], data: {} },
			A007: { color: "grey", state: true, path: ["m194.98 124.35 8.3314-0.10566 0.039 11.804-2.8834 2.3552-3.2482-0.56421-0.16096-8.1875-4.0636-0.42932 0.34421-5.1618 1.5774-0.0104z"], data: {} },
			A008: { color: "grey", state: true, path: ["m178.1 137.09c-0.10151 0.0892-5.2231 1.078-5.4791 1.078l8e-3 -4.1664 5.4587-5.2702z"], data: {} },
			A009: { color: "grey", state: true, path: ["m138.52 148.2c4.8685-5.163 9.822-10.24 14.804-15.293l0.14948 19.742-4.3884-0.38276-1.2629-0.4907-4.3858 0.82867z"], data: {} },
			tour: { color: "grey", state: true, path: ["m202.41 87.131c-3.0394-1.1048-1.2951-5.1697 1.3198-4.1201 2.7072 1.0866 1.0989 4.9993-1.3198 4.1201z"], data: {} }

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
  stroke-width:0.2px;
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
	