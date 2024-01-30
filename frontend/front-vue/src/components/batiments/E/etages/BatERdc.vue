<template>
	<div class="grid">
    <Selector
        current-floor="Rez-de-chaussée"
        :min="valMin"
        :max="valMax"
        :real-min="realMin"
        :real-max="realMax"
        :unit="unit"
        @updateSelectedOption="updateSelectedOption"
    ></Selector>
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
import dataScale from '../../utils/dataScale.vue';
import RoomDetail from '@/components/roomDetail/roomDetail.vue';
import Selector from "@/components/batiments/utils/selector.vue";
import loadApiConfig from '../../../../utils/api.js';


export default {
	components: {
    Selector,
		RoomDetail,
		dataScale
	},

	setup() {
		const apiBaseUrl = ref(null);
		const valMin = ref(0);
		const valMax = ref(500);
		const realMax = ref(500);
		const realMin = ref(0);
		const unit = ref("");

		const roomData = reactive({
      Autres: { color: "grey", state: true, path: ["M 200.96602,249.86911 5.9007839,249.50523 74.9936,176.86045 l 30.72025,0.0611 -0.0931,55.69863 94.29069,-0.33112 -0.15748,-55.17551 51.9988,-0.0818 -0.23047,43.29774 16.62386,-0.0845 -1.25177,88.40887 529.38299,-2.26938 -0.11038,21.97497 -579.14651,0.47977 z", "m 220.76042,377.00972 33.50628,0.15768 -0.4463,92.6294 -43.22862,0.0369 z m -3.34822,-47.46278 36.68808,-0.17387 0.25242,47.60303 -33.60593,-0.10044 z", "m 251.84328,176.99121 38.85182,0.2381 -0.60318,42.43195 -38.40852,0.53222 z"], data:{} },
      Tours: { color: "grey", state: true, path: ["M 270.63322,130.47864 A 33.973122,33.973122 0 0 1 236.6601,164.45176 33.973122,33.973122 0 0 1 202.68697,130.47864 33.973122,33.973122 0 0 1 236.6601,96.505516 33.973122,33.973122 0 0 1 270.63322,130.47864 Z", "m 868.78194,318.70521 a 34.231827,34.231827 0 0 1 -34.23183,34.23183 34.231827,34.231827 0 0 1 -34.23183,-34.23183 34.231827,34.231827 0 0 1 34.23183,-34.23182 34.231827,34.231827 0 0 1 34.23183,34.23182 z"], data:{} },
      Sanitaires: { color: "grey", state: true, path: ["m 105.73314,232.34519 0.0564,-55.42476 93.72306,0.0515 0.23196,55.08123 z"], data:{} },
      E070: { color: "grey", state: true, path: ["m 267.93042,220.26498 22.43882,-0.41443 0.55543,-42.63789 40.2879,-0.0393 -0.086,130.91679 -64.00262,0.25217 z"], data:{} },
      E001: { color: "grey", state: true, path: ["m 331.43366,177.07178 119.87758,-0.0111 0.0392,130.80775 -119.96028,0.33003 z"], data:{} },
      E002: { color: "grey", state: true, path: ["m 451.44091,177.12708 117.40877,-0.17805 0.48789,129.89591 -117.79788,0.7478 z"], data:{} },
      E003: { color: "grey", state: true, path: ["m 569.09,177.04468 123.01478,0.25416 0.0648,129.27832 -122.63651,0.29551 z"], data:{} },
      E004: { color: "grey", state: true, path: ["m 692.3,177.18234 127.69964,0.0189 -0.0193,99.15921 -23.60646,29.59767 -103.90467,0.69396 z"], data:{} },
      E005: { color: "grey", state: true, path: ["m 695.7136,329.36719 100.56832,0.14321 23.65283,31.18875 -0.0909,109.44822 -124.18719,-0.0611 z"], data:{} },
      E006: { color: "grey", state: true, path: ["m 576.00191,329.17425 119.52978,0.24614 -0.12896,140.68999 -119.41738,-0.055 z"], data:{} },
      E007: { color: "grey", state: true, path: ["m 394.68052,329.23352 181.29715,-0.0597 -0.0527,140.89553 -181.49782,-0.0781 z"], data:{} },
      E008: { color: "grey", state: true, path: ["m 254.06582,469.79721 0.25213,-140.4483 140.15065,-0.0797 -0.37,140.73793 z"], data:{} },

    });


		let selectedOption = 'activity';
		const roomName = ref(null);


    const updateSelectedOption = (selected) => {
      selectedOption = selected;
      updateColors();
    };

		const showRoomDetail = (roomId) => {
			roomName.value = roomId;
		};

		const fetchAllRoomData = async () => {
			try {
				const response = await fetch(`${apiBaseUrl.value}/ByRoom/?last_data=1&depth=1&floor=0&building=E`);
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
								state: true,
                battery: roomInfo.sensor.batterylevel,
							};
						} else {
							// Gérer le cas où les données de la salle ne sont pas disponibles
							roomData[roomId].state = false;
						}
					}
				}

				updateColors();
			} catch (error) {
				console.error('Erreur lors de la récupération des données des salles.', error);
			}
		};

		const updateColors = () => {
			for (const roomId in roomData) {
				if (roomData.hasOwnProperty(roomId) && roomData[roomId].state) {
					const metricValue = parseFloat(roomData[roomId]['data'][selectedOption]);

					if (!isNaN(metricValue)) {
						roomData[roomId].color = getColorForMetric(metricValue, selectedOption);

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
      if (option == "battery") {
        valMin.value = 0;
        valMax.value = 100;
        realMin.value = 0;
        realMax.value = 100;

        unit.value = "%";
        return `hsl(${value*1.2}, 100%, 50%)`;
      }
		};
		watch(
			() => selectedOption.value,
			() => {
				updateColors();
			}
		);


		onMounted(async () => {
			try {
				apiBaseUrl.value = await loadApiConfig();
				fetchAllRoomData();
			} catch (error) {
				console.error("Error while loading API config:", error);
			}
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