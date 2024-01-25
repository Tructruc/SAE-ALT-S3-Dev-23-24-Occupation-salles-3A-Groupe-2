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
		<svg width="100%%" height="100%" viewBox="-10 -10 950 390">
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
      Tours: { color: "grey", state: true, path: ["M 332.46997,35.007156 A 35.089081,35.089081 0 0 1 297.38089,70.096237 35.089081,35.089081 0 0 1 262.29181,35.007156 35.089081,35.089081 0 0 1 297.38089,-0.08192444 35.089081,35.089081 0 0 1 332.46997,35.007156 Z", "m 932.86257,229.02542 c 0,19.37916 -15.70992,35.08908 -35.08908,35.08908 -19.37916,0 -35.08908,-18.54793 -35.08908,-35.08908 0,-16.54115 15.70991,-35.08909 35.08908,-35.08909 19.37917,0 35.08909,15.70992 35.08908,35.08909 z"], data:{} },
      Autres: { color: "grey", state: true, path: ["m 125.54371,246.37606 0.0376,-32.45937 136.25339,0.0977 -0.19933,-132.243549 53.24828,0.0083 1.00506,132.342379 499.28891,-0.0878 -0.22005,-43.51639 15.96674,0.11079 0.4466,43.37241 26.35775,0.0801 -0.44451,32.46218 -146.64,0.10388 0.0542,30.76717 -109.17707,0.0844 0.0208,-31.00175 z", "m 253.97,273.7 0.0466,-27.13081 36.34326,0.0983 -0.0691,27.33186 z", "m 831.01772,170.63325 51.48999,0.23512 -0.12781,18.298 -24.72763,24.52893 -26.1831,0.20747 z", "m 314.98173,81.787015 36.18305,-0.01428 0.12184,37.320555 -20.84108,0.25521 0.18337,94.46713 -14.56322,0.059 z", "m 224.58,165.92 -50.78034,-0.35563 0.0173,-31.366 24.1411,-0.069 3.8505,5.5585 59.65322,-0.30935 0.0534,45.64452 -25.08725,-0.13908 z"], data:{} },
      Sanitaires: { color: "grey", state: true, path: ["m 201.9811,139.51332 -3.99085,-5.44674 -24.14515,0.0606 -0.007,-52.409936 87.45335,0.06827 0.16611,57.571896 z"], data:{} },
      E212: { color: "grey", state: true, path: ["m 224.56387,165.94671 11.7958,19.03563 25.08127,0.0637 0.17524,28.77196 -87.82456,0.0251 0.007,-48.19553 z"], data:{} },
      E268: { color: "grey", state: true, path: ["m 710.72932,246.69674 45.63848,-0.0244 -0.0135,132.01279 -45.51245,0.0181 z"], data:{} },
      E267: { color: "grey", state: true, path: ["m 756.39705,246.6621 61.74274,0.0202 0.0174,131.97821 -61.73852,0.0135 z"], data:{} },
      E266: { color: "grey", state: true, path: ["m 818.25612,246.65894 38.98698,-0.0524 25.35431,19.95899 -0.0364,112.12465 -64.3085,-0.0169 z"], data:{} },
      E211: { color: "grey", state: true, path: ["m 125.59296,213.6784 -0.0235,-22.0521 -65.27524,-0.11384 -20.953808,-19.66717 94.321898,-90.102402 40.15585,-0.02501 -0.05,132.131172 z"], data:{} },
      E269: { color: "grey", state: true, path: ["M 710.69158,277.42997 710.54684,378.6824 639.77002,378.627 639.60651,277.51344 Z"], data:{} },
      E270: { color: "grey", state: true, path: ["m 601.47653,277.54809 38.04314,-0.007 0.11891,101.09512 -38.11761,0.0707 z"], data:{} },
      E265: { color: "grey", state: true, path: ["m 815.15381,81.835409 67.14719,-0.04735 v 89.126951 l -67.32242,-0.48593 z"], data:{} },
      E264: { color: "grey", state: true, path: ["m 762.15699,103.40517 52.76298,0.057 -0.008,110.40345 -52.73715,-0.0696 z"], data:{} },
      E263: { color: "grey", state: true, path: ["m 698.84,103.35 63.20278,0.1004 -0.0576,110.35472 -63.15942,-0.0242 z"], data:{} },
      E262: { color: "grey", state: true, path: ["m 611.36268,213.85333 0.0101,-110.44733 87.26077,-0.5645 -0.0147,110.94546 z"], data:{} },
      E261: { color: "grey", state: true, path: ["m 611.27276,103.39669 0.002,110.46795 -89.50704,-0.005 0.0111,-110.44196 z"], data:{} },
      E260: { color: "grey", state: true, path: ["m 456.86887,103.44917 64.85039,-0.0578 -0.007,110.48118 -64.84115,0.0274 z"], data:{} },
      E206: { color: "grey", state: true, path: ["m 330.58268,119.58703 20.87559,-0.20453 -0.26632,-37.596696 105.77433,0.01253 -0.14562,132.087076 -126.06786,-0.0914 z"], data:{} },
      E209: { color: "grey", state: true, path: ["m 125.54266,246.50549 128.36071,0.076 -0.0915,27.25217 36.48578,0.34019 0.17392,104.49099 -164.93415,0.0126 z"], data:{} },
      E208: { color: "grey", state: true, path: ["m 290.47361,246.66535 168.04639,0.33835 0.12726,131.68049 -168.10888,-0.006 z"], data:{} },
      E210: { color: "grey", state: true, path: ["M 0.07196104,378.66049 0,207.08 l 39.194537,-35.08697 20.906722,19.63042 65.383151,0.0993 0.005,186.95076 z"], data:{} },
      E207: { color: "grey", state: true, path: ["m 458.72633,246.64466 142.52367,0.16236 0.16273,131.87826 -142.66236,-0.007 z"], data:{} },

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