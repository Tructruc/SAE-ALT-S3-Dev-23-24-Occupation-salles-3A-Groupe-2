<!-- Template de header pour les pages ( barre de recherche ) -->
<!-- Le composant est modulaire et ne doit pas dépendre du reste de l'application -->
<template>
  <div class="header">

    <div class="headerButtonContainer">
        <!-- on met des liens vers la page d'accueil de google-->
        <button @click="changeView('FullIut')">Accueil</button>
        <button @click="changeView('ListeSalles')">Salles</button>

    </div>
    
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Rechercher salle ...">
        <button type="submit" class="search-button">
          <svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px"><path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/></svg>
        </button>


    </div>
    </div>
</template>

<script>
export default {
  name: 'Header',
  methods: {
    changeView(view) {
      this.$emit('changeView', view);
    }
  }
};
</script>

<style>
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
    display: flex;
    width: 30%;
    overflow: hidden;
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
    color: var(--color-inverted-text);
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
    fill: var(--color-inverted-text);
    border: none;
}

.search-button svg:hover {
    fill: var(--color-text-hover);
}


.headerButtonContainer button {
    background-color: var(--color-inverted-background-hard);
    color: var(--color-inverted-text);
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

.headerButtonContainer {
    display: flex;
    align-items: center;
}


</style>