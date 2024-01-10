<!-- Template de header pour les pages ( barre de recherche ) -->
<!-- Le composant est modulaire et ne doit pas dépendre du reste de l'application -->
<template>
  <div class="header">
    <div class="header__search">
      <input
        type="text"
        placeholder="Rechercher une salle"
        v-model="search"
        @keyup.enter="rechercherSalle"
      />
      <button @click="rechercherSalle">
        <i class="fas fa-search"></i>
      </button>
    </div>
    <div class="header__links">

      <router-link to="/carte">
        <i class="Carte"></i>
        <span class="Carte">Carte</span>
      </router-link>

    </div>
  </div>
</template>

<style>
.header {

    position: fixed;
    top: 0;
    left: 0;


    width:100%;
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #fff;
    color:black;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.header__search {
    display: flex;
    align-items: center;
    border-radius: 5px;
    overflow: hidden;
    border: 1px solid #ccc;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>