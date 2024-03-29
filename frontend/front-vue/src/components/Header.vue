<template>
  <div class="header">
    <div class="headerButtonContainer">
      <button @click="changeView('FullIut')">Accueil</button>
      <button @click="changeView('ListeSalles')">Salles</button>
    </div>

    <div class="title">
      <div class="logo-container">
        <img src="@/assets/logo.webp" alt="Logo" class="header-logo">
      </div>
      <h1>
        Dashboard de surveillance des salles
      </h1>
    </div>

    <div class="search-container">
      <input
        type="text"
        class="search-input"
        v-model="searchQuery"
        @input="fetchSuggestions"
        @keydown="handleKeydown"
        ref="searchInput"
        placeholder="Rechercher salle ..."
      />
      <!-- Modification: Ajout de && searchQuery à la condition v-if -->
      <ul ref="suggestionsContainer" v-if="suggestions.length && searchQuery" class="suggestions">
        <li
          v-for="(suggestion, index) in suggestions"
          :key="suggestion"
          @click="performSearch(suggestion)"
          @mouseenter="highlightedIndex = index"
          :class="{ active: index === highlightedIndex }"
        >
          {{ suggestion }}
        </li>
      </ul>
      <button
        ref="searchButton"
        type="submit"
        class="search-button"
        @click="performSearch(searchQuery)"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 50 50"
          width="50px"
          height="50px"
        >
          <path
            d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import loadApiConfig from '../utils/api.js';

export default {
  name: "Header",
  data() {
    return {
      searchQuery: "",
      suggestions: [],
      highlightedIndex: -1,
      apiBaseUrl: null,
    };
  },
  methods: {
    hideSuggestions() {
      this.suggestions = [];
      this.highlightedIndex = -1;
      this.searchQuery = "";
    },
    handleClickOutside(event) {
      if (this.$refs.searchInput && !this.$refs.searchInput.contains(event.target) &&
          this.$refs.searchButton && !this.$refs.searchButton.contains(event.target)) {
        this.hideSuggestions();
      }
    },
    handleEscape(event) {
      if (event.key === 'Escape') {
        this.hideSuggestions();
      }
    },
    changeView(view, props = {}) {
      this.$emit("changeView", view, props);
    },
    fetchSuggestions() {
      if (this.searchQuery) {
          this.highlightedIndex = 0;
          fetch(`${this.apiBaseUrl}/AutoCompletSearch?q=${this.searchQuery}`)
              .then((response) => response.json())
              .then((data) => (this.suggestions = data))
              .catch((error) => console.error("Error:", error));
      } else {
          this.suggestions = [];
      }
    },
    performSearch(searchTerm) {
      this.searchQuery = searchTerm; // Modification: Mise à jour de searchQuery
      this.suggestions = []; // Ajout: Vider les suggestions lors de la recherche
      fetch(`${this.apiBaseUrl}/Search?q=${this.searchQuery}`)
        .then((response) => response.json())
        .then((data) => {
          // Si le tableau est de longeur 1
          if (data.length === 1) {
            this.changeView("roomDetail", { room: data[0].room});
            document.getElementsByClassName("search-input")[0].value = ""; // Modification: Vider le champ de recherche
          } else {
            // Modification: Afficher la liste des salles trouvées
            this.$emit("showRoomList", data);
          }
        });
    },
    handleKeydown(event) {
      let container, activeItem, itemHeight, containerHeight, scrollPosition, itemPosition;

      switch (event.key) {
        case 'ArrowDown':
          this.highlightedIndex = (this.highlightedIndex + 1) % this.suggestions.length;
          break;
        case 'ArrowUp':
          this.highlightedIndex = (this.highlightedIndex - 1 + this.suggestions.length) % this.suggestions.length;
          break;
        case 'Enter':
          if (this.highlightedIndex >= 0) {
            this.performSearch(this.suggestions[this.highlightedIndex]);
            this.highlightedIndex = -1; // Reset the index
          }
          break;
      }

      container = this.$refs.suggestionsContainer; // Add a ref to your ul element
      try {
        activeItem = container.children[this.highlightedIndex];
      } catch (e) {
        // Do nothing if there is no active item
      }
      if (activeItem) {
        itemHeight = activeItem.offsetHeight;
        containerHeight = container.offsetHeight;
        scrollPosition = container.scrollTop;
        itemPosition = activeItem.offsetTop;

        if (itemPosition + itemHeight > scrollPosition + containerHeight) {
          // Scroll down
          container.scrollTop = itemPosition + itemHeight - containerHeight;
        } else if (itemPosition < scrollPosition) {
          // Scroll up
          container.scrollTop = itemPosition;
        }
      }
    },
  },
  mounted() {
    loadApiConfig().then(apiIp => {
      this.apiBaseUrl = apiIp;
    }).catch(error => {
      console.error("Error while loading API config:", error);
    });

    document.addEventListener('click', this.handleClickOutside);
    document.addEventListener('keydown', this.handleEscape);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
    document.removeEventListener('keydown', this.handleEscape);
  },
};
</script>



<style scoped>
  .header {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 80px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 2rem;
      background-color: var(--color-inverted-background-mute);
      color: black;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
      z-index: 1000;
  }

  .header > div {
      display: flex;
      align-items: center;
  }

  .search-container {
      position: relative;
      width: 30%;
      border-radius: 5px;
      margin-left: auto; /* Push the search container to the right */
  }

  .search-input {
      flex: 1;
      padding: 10px;
      border: none;
      border-radius: 5px 0 0 5px;
      font-size: 16px;
      height: 45px;
  }

  .search-button {
      background-color: var(--color-inverted-background-hard);
      color: var(--vt-c-text-dark-1);
      border: none;
      cursor: pointer;
      border-radius: 0 5px 5px 0;
      font-size: 16px;
      transition: background-color 0.3s ease;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 45px;
  }

  .search-button svg {
      margin: 5px;
      height: 35px;
      fill: var(--vt-c-text-dark-1);
      border: none;
  }

  .search-button svg:hover {
      fill: var(--color-text-hover);
  }


  .headerButtonContainer button {
      background-color: var(--color-inverted-background-hard);
      color: var(--vt-c-text-dark-1);
      border: none;
      padding: 10px 15px;
      cursor: pointer;
      border-radius: 5px;
      font-size: 16px;
      margin-right: 10px;
      transition: background-color 0.3s ease;
  }

  .header button:hover {
      background-color: var(--color-background-hover);
      color: var(--color-text-hover);
  }

  .title {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    color: var(--color-inverted-text);
  }

  .headerButtonContainer {
      display: flex;
      align-items: center;
  }

  /* Styles pour la liste des suggestions */
  .suggestions {
      top: 100%;
      list-style-type: none;
      position: absolute;
      width: 100%; /* La largeur correspond à celle de l'input */
      background-color: white;
      box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
      border-radius: 0 0 5px 5px;
      margin-top: 2px;
      max-height: 200px; /* Hauteur maximale fixée à 200px */
      overflow-y: auto; /* Permet le scrolling vertical */
      z-index: 1000;
      padding: 0px;
  }

  .suggestions li {
      padding: 10px;
      cursor: pointer;
      border-bottom: 1px solid #eee;
  }

  /* Style au survol des éléments de la liste */
  .suggestions li:hover {
      background-color: #e6e6e6;
  }

  .suggestions li.active {
      background-color: #e6e6e6;
  }

  /* Pas de bordure en bas pour le dernier élément */
  .suggestions li:last-child {
      border-bottom: none;
  }

  .header-logo {
      height: 60px; /* Ajustez la hauteur selon vos besoins */
      margin-right: 20px; /* Espace entre le logo et le titre */
      border-radius: 10px;
  }

  .logo-container {
      display: flex;
      align-items: center;
  }
</style>