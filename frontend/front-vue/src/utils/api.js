// Fonction pour charger le fichier api.json
function loadApiConfig() {
    return fetch('../assets/api.json') // Assurez-vous que le chemin est correct
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(apiConfig => {
        console.log("apiConfig: ", apiConfig);
        console.log("apiConfig.API_URL: ", apiConfig.API_URL);
  
        if (!apiConfig.API_URL || apiConfig.API_URL === "$API_URL") {
          return "http://localhost:8000";
        } else {
          console.log("Using API_URL from api.json");
          return apiConfig.API_URL;
        }
      })
      .catch(error => {
        console.error('Error loading api.json:', error);
        return "http://localhost:8000";
      });
  }
  
  export default loadApiConfig;
  